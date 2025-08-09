export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100svh-theme(spacing.16))]">
      <h1 className="text-4xl font-bold mb-4">Welcome to Business Management Suite</h1>
      <p className="text-lg text-gray-600">Select a page from the sidebar to get started.</p>
      <div className="mt-8 p-6 bg-gray-100 rounded-lg shadow-md text-center">
        <h2 className="text-2xl font-semibold mb-2">Dashboard Overview</h2>
        <p className="text-gray-700">This is your central hub for all business operations.</p>
        <p className="text-sm text-gray-500 mt-2">
          Use the navigation on the left to explore different modules like Calendar, Invoices, Customers, and more.
        </p>
      </div>
    </div>
  )
}
