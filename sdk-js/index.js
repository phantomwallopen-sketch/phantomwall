export async function guard(opts = {}) {
  const { endpoint = 'http://127.0.0.1:8000/v1/guard', policy = 'strict', telemetry = false } = opts;

  async function check(user_input, context = {}) {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_input, policy, context })
    });
    if (!res.ok) throw new Error('PhantomWall endpoint error');
    return await res.json();
  }

  return { check };
}
