"use client";

import Image from 'next/image';
import Link from 'next/link';
import { useAuth } from '@/components/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return (
    <nav className="navbar-bg flex items-center justify-between px-6 py-1">
      {/* Logo - Left */}
      <div className="flex items-center">
        <Link href="/">
          <Image src="/logoandtext.png" alt="Heater Logo" width={180} height={60} />
        </Link>
      </div>

      {/* Navigation Links - Center */}
      <div className="flex items-center space-x-2">
        <Link 
          href="/picks" 
          className="text-white text-lg font-bold hover:bg-white hover:text-black px-8 py-3 transition-all tracking-wide"
        >
          MAKE PICKS
        </Link>
        <Link 
          href="/leaderboard" 
          className="text-white text-lg font-bold hover:bg-white hover:text-black px-8 py-3 transition-all tracking-wide"
        >
          LEADERBOARD
        </Link>
        <Link 
          href="/history" 
          className="text-white text-lg font-bold hover:bg-white hover:text-black px-8 py-3 transition-all tracking-wide"
        >
          HISTORY
        </Link>
      </div>

      {/* Right Section - Profile/Auth */}
      <div className="flex items-center space-x-3">
        {user ? (
          <>
            {/* Show when logged in */}
            <Link 
              href="/profile" 
              className="text-gray-300 hover:text-white hover:bg-gray-800 px-4 py-2 rounded-lg transition-all font-medium"
            >
              Profile
            </Link>
            <span className="text-gray-400 text-sm px-3 py-2 bg-gray-800 rounded-lg">
              {user.email}
            </span>
            <button 
              onClick={handleLogout}
              className="bg-gray-700 text-white px-4 py-2 rounded-lg font-semibold hover:bg-gray-600 transition-colors"
            >
              Sign Out
            </button>
          </>
        ) : (
          <>
            {/* Show when logged out */}
            <Link 
              href="/login" 
              className="bg-[#ff9f1c] text-black px-5 py-2 rounded-lg font-semibold hover:bg-[#e8900a] transition-colors shadow-md"
            >
              Sign In
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}