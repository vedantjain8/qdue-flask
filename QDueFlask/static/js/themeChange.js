const themeSwitchBtn = document.getElementById('themeToggleBtn');
const storedTheme = localStorage.getItem('theme');
const themeIcon = document.getElementById('themeIcon');
const themeIconAlt = document.getElementById('themeIconAlt');

if (storedTheme) {
  // Remove any existing theme classes
  document.body.classList.remove('light-theme', 'dark-theme');

  // Add the stored theme class
  document.body.classList.add(storedTheme);

  // Set the initial icon based on the stored theme
  if (storedTheme === 'dark-theme') {
    themeIcon.style.display = 'none';
    themeIconAlt.style.display = 'inline-block';
  }
  
  // Change the icon based on the current theme
  else {
    themeIcon.style.display = 'inline-block';
    themeIconAlt.style.display = 'none';
  }
} else {
  localStorage.setItem('theme', 'light-theme');
}

themeSwitchBtn.addEventListener('click', function () {
  document.body.classList.toggle('light-theme');
  document.body.classList.toggle('dark-theme');

  // Toggle the icons on each click
  themeIcon.style.display = themeIcon.style.display === 'none' ? 'inline-block' : 'none';
  themeIconAlt.style.display = themeIconAlt.style.display === 'none' ? 'inline-block' : 'none';

  // Update the stored theme based on the current class
  const currentTheme = document.body.classList.contains('light-theme') ? 'light-theme' : 'dark-theme';
  localStorage.setItem('theme', currentTheme);
 
});