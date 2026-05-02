export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-zinc-100">
      <div className="flex">
        <aside className="w-64 min-h-screen bg-zinc-900 text-white p-6">
          <h2 className="text-xl font-bold">RSS Admin</h2>

          <nav className="mt-8 flex flex-col gap-3 text-sm">
            <a href="/overview">Dashboard</a>
            <a href="/facturas">Facturas</a>
            <a href="/pagos-bac">Pagos BAC</a>
            <a href="/cai-correlativos">CAI / Correlativos</a>
            <a href="/plantilla-factura">Plantilla Factura</a>
            <a href="/storeganise">Storeganise</a>
            <a href="/reportes">Reportes</a>
            <a href="/alertas">Alertas</a>
          </nav>
        </aside>

        <main className="flex-1 p-8">{children}</main>
      </div>
    </div>
  );
}