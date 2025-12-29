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
      bg: 'bg-[#10B981]',
      text: 'text-white',
      border: 'border-[#10B981]'
    },
    Medium: {
      bg: 'bg-[#F59E0B]',
      text: 'text-white',
      border: 'border-[#F59E0B]'
    },
    High: {
      bg: 'bg-[#EF4444]',
      text: 'text-white',
      border: 'border-[#EF4444]'
    }
  };

  const styles = riskStyles[riskLevel] || riskStyles.Low;

  return (
    <div className={`${styles.bg} ${styles.text} rounded-lg p-6 md:p-8 text-center shadow-lg`}>
      <div className="text-3xl md:text-4xl font-bold mb-2">
        {riskLevel} Risk
      </div>
      <div className="text-lg md:text-xl opacity-90">
        {confidence}% Confidence
      </div>
    </div>
  );
}

