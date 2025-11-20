import Image from 'next/image';
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="navbar-bg flex items-center justify-between px-6 py-3">
      {/* Logo - Left */}
      <div className="flex items-center">
        <Link href="/">
          <Image src="/logoandtext.png" alt="Heater Logo" width={200} height={70} />
        </Link>
      </div>

      {/* Navigation Links - Center */}
      <div className="flex items-center space-x-8">
        <Link href="/picks" className="text-white hover:text-[#ff9f1c] transition-colors">
          Make Picks
        </Link>
        <Link href="/leaderboard" className="text-white hover:text-[#ff9f1c] transition-colors">
          Leaderboard
        </Link>
        <Link href="/leagues" className="text-white hover:text-[#ff9f1c] transition-colors">
          Leagues
        </Link>
        <Link href="/history" className="text-white hover:text-[#ff9f1c] transition-colors">
          History
        </Link>
      </div>

      {/* Right Section - Profile/Auth */}
      <div className="flex items-center space-x-4">
        <Link href="/profile" className="text-white hover:text-[#ff9f1c] transition-colors">
          Profile
        </Link>
        <button className="bg-[#ff9f1c] text-black px-4 py-2 rounded-lg font-semibold hover:bg-[#e8900a] transition-colors">
          Sign In
        </button>
      </div>
    </nav>
  );
}