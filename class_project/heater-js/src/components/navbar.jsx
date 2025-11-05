import Image from 'next/image'
export default function Navbar() {
  return (
            <nav className="navbar-bg">
                <div className="flex items-center">
                    <Image src="/logoandtext.png" alt="Heater Logo" width={200} height={70} />
                </div>
            </nav>
  )
}