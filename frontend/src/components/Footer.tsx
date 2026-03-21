export function Footer() {
  return (
    <footer className="mt-12 border-t border-gray-200 bg-white py-6">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <p className="text-center text-sm text-gray-400">
          Data: Gemeente Amsterdam &middot; Kaartgegevens &copy;{" "}
          <a
            href="https://www.openstreetmap.org/copyright"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-600"
          >
            OpenStreetMap
          </a>{" "}
          contributors &middot;{" "}
          <a
            href="https://github.com/dunnkers/zwemmr"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-600"
          >
            GitHub
          </a>
        </p>
      </div>
    </footer>
  );
}
