/**
 * Reusable Button Component
 * @param {Object} props - Component props
 * @param {string} props.variant - Button style variant (primary, secondary, outline)
 * @param {string} props.size - Button size (sm, md, lg)
 * @param {boolean} props.disabled - Disable button
 * @param {Function} props.onClick - Click handler
 * @param {React.ReactNode} props.children - Button content
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children,
  className = '',
  type = 'button'
}) {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-[#2563EB] text-white hover:bg-[#1D4ED8] focus:ring-[#2563EB]',
    secondary: 'bg-[#10B981] text-white hover:bg-[#059669] focus:ring-[#10B981]',
    outline: 'bg-transparent border-2 border-[#2563EB] text-[#2563EB] hover:bg-[#2563EB] hover:text-white focus:ring-[#2563EB]',
    danger: 'bg-[#EF4444] text-white hover:bg-[#DC2626] focus:ring-[#EF4444]'
  };

  const sizes = {
    sm: 'h-10 px-4 text-sm',
    md: 'h-12 px-6 text-base',
    lg: 'h-14 px-8 text-lg'
  };

  const classes = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

