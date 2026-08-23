import { loginWithGoogle } from "../services/api";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="bg-white rounded-xl shadow p-10 text-center max-w-sm">
        <h1 className="text-2xl font-bold mb-2">Resume Enhancer</h1>
        <p className="text-gray-500 mb-6">Sign in to generate tailored resumes.</p>
        <button
          onClick={loginWithGoogle}
          className="w-full px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium"
        >
          Sign in with Google
        </button>
      </div>
    </div>
  );
}