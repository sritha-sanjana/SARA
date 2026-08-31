import type { SARAResponse } from '../types/sara';

// Use environment variable for API base URL; falls back to empty string (relative path) for local development
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function analyzeCase(caseText: string): Promise<SARAResponse> {
  const trimmed = caseText.trim();
  if (!trimmed) {
    throw new Error('Case text cannot be empty.');
  }

  const controller = new AbortController();
  // SARA pipeline executes multiple LLM calls sequentially; allow 120s timeout
  const timeoutId = setTimeout(() => controller.abort(), 120000);

  try {
    const analyzeUrl = `${API_BASE_URL}/analyze`;
    const response = await fetch(analyzeUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ case_text: trimmed }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      let errorDetail = `Server error (${response.status})`;
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          errorDetail = typeof errorData.detail === 'string'
            ? errorData.detail
            : JSON.stringify(errorData.detail);
        }
      } catch {
        if (response.statusText) {
          errorDetail = `${response.status} ${response.statusText}`;
        }
      }
      throw new Error(errorDetail);
    }

    const data: SARAResponse = await response.json();
    return data;
  } catch (err: unknown) {
    clearTimeout(timeoutId);
    if (err instanceof Error) {
      if (err.name === 'AbortError') {
        throw new Error('The analysis request timed out after 2 minutes. Please verify your backend server or try again.');
      }
      throw err;
    }
    throw new Error('An unexpected error occurred during case analysis.');
  }
}
