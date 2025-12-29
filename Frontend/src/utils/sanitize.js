/**
 * Input Sanitization Utilities
 * Protects against XSS attacks and validates input
 */

/**
 * Sanitize text input by removing potentially dangerous characters
 * @param {string} input - User input string
 * @returns {string} Sanitized string
 */
export function sanitizeText(input) {
  if (typeof input !== 'string') return '';
  
  return input
    .replace(/[<>]/g, '') // Remove < and > to prevent HTML injection
    .trim()
    .slice(0, 10000); // Limit length to prevent DoS
}

/**
 * Sanitize biological sequence input
 * Allows only valid DNA/RNA/Protein characters
 * @param {string} sequence - Biological sequence
 * @returns {string} Sanitized sequence
 */
export function sanitizeSequence(sequence) {
  if (typeof sequence !== 'string') return '';
  
  // Allow DNA/RNA bases (A, T, G, C, U) and protein amino acids (standard 20)
  // Also allow common sequence format characters (spaces, newlines, numbers for positions)
  const allowedPattern = /^[ATGCNURYSWKMBDHVZ\s\n\r0-9]*$/i;
  
  // Remove any characters that don't match the pattern
  let sanitized = sequence
    .split('')
    .filter(char => allowedPattern.test(char))
    .join('')
    .trim();
  
  // Limit length
  return sanitized.slice(0, 50000);
}

/**
 * Validate and sanitize age input
 * @param {any} age - Age input
 * @returns {number|null} Valid age or null
 */
export function sanitizeAge(age) {
  const num = parseInt(age, 10);
  if (isNaN(num) || num < 18 || num > 100) {
    return null;
  }
  return num;
}

/**
 * Validate smoking history selection
 * @param {string} value - Selected value
 * @returns {string|null} Valid value or null
 */
export function sanitizeSmokingHistory(value) {
  const validValues = ['Never', 'Former Smoker', 'Current Smoker'];
  return validValues.includes(value) ? value : null;
}

/**
 * Validate gender selection
 * @param {string} value - Selected value
 * @returns {string|null} Valid value or null
 */
export function sanitizeGender(value) {
  const validValues = ['Male', 'Female', 'Other'];
  return validValues.includes(value) ? value : null;
}

/**
 * Escape HTML to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
export function escapeHtml(text) {
  if (typeof text !== 'string') return '';
  
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  
  return text.replace(/[&<>"']/g, m => map[m]);
}

