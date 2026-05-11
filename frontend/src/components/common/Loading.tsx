import { Spin } from 'antd';

interface LoadingProps {
  fullscreen?: boolean;
  tip?: string;
}

export default function Loading({ fullscreen = false, tip = 'Loading...' }: LoadingProps) {
  if (fullscreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white bg-opacity-90 z-50">
        <Spin size="large" tip={tip} />
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center py-12">
      <Spin size="large" tip={tip} />
    </div>
  );
}
