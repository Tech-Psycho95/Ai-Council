const mongoose = require('mongoose');

const rateLimitSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    lowercase: true,
    trim: true,
    index: true
  },
  action: {
    type: String,
    required: true,
    enum: ['forgot-password', 'login-attempt', 'register'],
    index: true
  },
  ipAddress: {
    type: String
  },
  userAgent: {
    type: String
  },
  success: {
    type: Boolean,
    default: true
  },
  createdAt: {
    type: Date,
    default: Date.now,
    expires: 3600 // Auto-delete after 1 hour
  }
});

// Compound index for efficient queries
rateLimitSchema.index({ email: 1, action: 1, createdAt: 1 });

// Static method to check rate limit
rateLimitSchema.statics.checkRateLimit = async function(email, action, maxAttempts = 3, windowMs = 3600000) {
  const windowStart = new Date(Date.now() - windowMs);
  
  const count = await this.countDocuments({
    email: email.toLowerCase(),
    action,
    createdAt: { $gte: windowStart }
  });
  
  return {
    allowed: count < maxAttempts,
    remaining: Math.max(0, maxAttempts - count),
    resetAt: new Date(windowStart.getTime() + windowMs)
  };
};

// Static method to log an attempt
rateLimitSchema.statics.logAttempt = async function(email, action, ipAddress, userAgent, success = true) {
  return this.create({
    email: email.toLowerCase(),
    action,
    ipAddress,
    userAgent,
    success
  });
};

// Static method to get recent attempts for security monitoring
rateLimitSchema.statics.getRecentAttempts = async function(email, action, hours = 24) {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000);
  
  return this.find({
    email: email.toLowerCase(),
    action,
    createdAt: { $gte: since }
  }).sort({ createdAt: -1 });
};

module.exports = mongoose.model('RateLimit', rateLimitSchema);
