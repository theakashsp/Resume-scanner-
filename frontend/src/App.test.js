import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Resume Analyzer branding', () => {
  render(<App />);
  expect(screen.getAllByText(/Resume/i).length).toBeGreaterThan(0);
  expect(screen.getAllByText(/Analyzer/i).length).toBeGreaterThan(0);
});
