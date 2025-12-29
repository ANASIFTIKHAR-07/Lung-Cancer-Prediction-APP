/**
 * Risk Level Badge Component
 * Displays risk level with color-coded styling
 * @param {Object} props - Component props
 * @param {string} props.riskLevel - Risk level (Low, Medium, High)
 * @param {number} props.confidence - Confidence percentage (0-100)
 */
export default function RiskBadge({ riskLevel, confidence }) {
  const riskStyles = {
    Low: {
      bg: 'bg-low-risk',
      text: 'text-white',
      border: 'border-low-risk'
    },
    Medium: {
      bg: 'bg-medium-risk',
      text: 'text-white',
      border: 'border-medium-risk'
    },
    High: {
      bg: 'bg-high-risk',
      text: 'text-white',
      border: 'border-high-risk'
    }
  };

  const styles = riskStyles[riskLevel] || riskStyles.Low;

  return (
    <div className={`${styles.bg} ${styles.text} rounded-xl p-6 md:p-8 text-center shadow-large`}>
      <div className="text-3xl md:text-4xl font-bold mb-2">
        {riskLevel} Risk
      </div>
      <div className="text-lg md:text-xl opacity-90">
        {confidence}% Confidence
      </div>
    </div>
  );
}

