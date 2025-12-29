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
    primary: 'bg-primary text-white hover:bg-primary-dark focus:ring-primary shadow-medium hover:shadow-large transition-all',
    secondary: 'bg-secondary text-white hover:bg-secondary-dark focus:ring-secondary shadow-medium hover:shadow-large transition-all',
    outline: 'bg-transparent border-2 border-primary text-primary hover:bg-primary hover:text-white focus:ring-primary transition-all',
    danger: 'bg-high-risk text-white hover:bg-high-risk/90 focus:ring-high-risk shadow-medium hover:shadow-large transition-all'
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

