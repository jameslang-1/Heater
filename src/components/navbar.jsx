import Image from 'next/image';
import Link from 'next/link';
export default function Navbar() {
  return (
            <nav className="navbar-bg">
                <div className="flex items-center">
                    <Image src="/logoandtext.png" alt="Heater Logo" width={200} height={70} />
                </div>
                <div className="flex items-center space-x-4">
                  <Link href="/picks" className="text-white hover:text-[#ff9f1c]">
                    Make Picks
                  </Link>
                </div>
            </nav>
  )
}