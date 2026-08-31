import type { SARAResponse } from '../types/sara';

export async function analyzeCase(caseText: string): Promise<SARAResponse> {
  const trimmed = caseText.trim();
  if (!trimmed) {
    throw new Error('Case text cannot be empty.');
  }

  const controller = new AbortController();
  // SARA pipeline executes multiple LLM calls sequentially; allow 120s timeout
  const timeoutId = setTimeout(() => controller.abort(), 120000);

  try {
    const response = await fetch('/analyze', {
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
