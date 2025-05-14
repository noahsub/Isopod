from textual.theme import Theme

LAVENDER = Theme(
    name='lavender',
    primary='#957fef',  # Warm yellow for highlights
    secondary='#8EC07C',  # Soft green for secondary text
    accent='#D3869B',  # Soft pink for accents
    foreground='#EBDBB2',  # Light beige for main text
    background='#282828',  # Dark warm gray for background
    success='#8EC07C',  # Light green for success
    warning='#D65D0E',  # Warm orange for warnings
    error='#CC241D',  # Deep red for errors
    surface='#32302F',  # Slightly lighter dark for panels
    panel='#3C3836',  # Darker gray for panel background
    dark=True,
    variables={
        'block-cursor-text-style': 'none',
        'footer-key-foreground': '#A89984',  # Muted gray for footer keys
        'input-selection-background': '#D3869B 35%',  # Light pink selection background
    },
)
