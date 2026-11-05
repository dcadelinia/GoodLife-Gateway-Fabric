export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body> {/* ◄ MUST BE PRESENT */}
    </html>
  )
}
