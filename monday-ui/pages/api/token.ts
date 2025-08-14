import type { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const mock = process.env.NEXT_PUBLIC_LIVEKIT_MOCK_TOKEN || 'mock-livekit-token';
  res.status(200).json({ ok: true, token: mock });
}
