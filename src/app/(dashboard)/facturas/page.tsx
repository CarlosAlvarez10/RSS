"use client";

import { useMemo, useState } from "react";
import { PageHeader } from "@/components/page-header";
import { StatusBadge, statusTone } from "@/components/status-badge";
import { ActionButton, EmptyState, SelectInput, TextInput } from "@/components/ui";
import { invoices, money, shortDate } from "@/lib/dashboard-data";

export default function FacturasPage() {
  const [client, setClient] = useState("");
  const [status, setStatus] = useState("TODOS");
  const [date, setDate] = useState("");
  const [message, setMessage] = useState("");

  const filtered = useMemo(() => {
    return invoices.filter((invoice) => {
      const matchClient = invoice.client.toLowerCase().includes(client.toLowerCase()) || invoice.email.toLowerCase().includes(client.toLowerCase());
      const matchStatus = status === "TODOS" || invoice.emailStatus === status;
      const matchDate = !date || invoice.issuedAt.startsWith(date);
      return matchClient && matchStatus && matchDate;
    });
  }, [client, status, date]);

  const downloadInvoice = (number: string) => {
    setMessage(`PDF de factura ${number} preparado para descarga.`);
    window.print();
  };

  const resendInvoice = (number: string, email: string) => {
    setMessage(`Factura ${number} reenviada a ${email}.`);
  };

  return (
    <>
      <PageHeader
        title="Facturas"
        description="Solo consulta de facturas generadas automáticamente después de pagos confirmados. Aquí no se crean facturas manualmente."
      />
      <div className="space-y-5 p-5">
        <section className="no-print grid gap-3 rounded-lg border border-slate-200 bg-white p-4 md:grid-cols-4">
          <TextInput placeholder="Filtrar por cliente o correo" value={client} onChange={(event) => setClient(event.target.value)} />
          <TextInput type="date" value={date} onChange={(event) => setDate(event.target.value)} />
          <SelectInput value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="TODOS">Todos los estados</option>
            <option value="ENVIADA">Enviada</option>
            <option value="PENDIENTE">Pendiente</option>
            <option value="FALLIDA">Fallida</option>
          </SelectInput>
          <ActionButton variant="secondary" onClick={() => { setClient(""); setStatus("TODOS"); setDate(""); }}>
            Limpiar filtros
          </ActionButton>
        </section>

        {message ? <div className="no-print rounded-lg border border-sky-200 bg-sky-50 p-3 text-sm font-bold text-sky-700">{message}</div> : null}

        <section className="rounded-lg border border-slate-200 bg-white">
          <div className="border-b border-slate-200 p-4">
            <h2 className="font-black text-slate-950">Listado de facturas generadas</h2>
          </div>
          {filtered.length === 0 ? (
            <div className="p-4"><EmptyState text="No hay facturas con esos filtros." /></div>
          ) : (
            <div className="overflow-x-auto">
              <table>
                <thead>
                  <tr>
                    <th>Número</th>
                    <th>Cliente</th>
                    <th>RTN</th>
                    <th>Correo</th>
                    <th>Monto</th>
                    <th>ISV</th>
                    <th>Total</th>
                    <th>CAI / Correlativo</th>
                    <th>Emisión</th>
                    <th>Correo</th>
                    <th>Referencia BAC</th>
                    <th className="no-print">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((invoice) => (
                    <tr key={invoice.id}>
                      <td className="font-mono">{invoice.number}</td>
                      <td className="font-bold text-slate-900">{invoice.client}</td>
                      <td>{invoice.rtn}</td>
                      <td>{invoice.email}</td>
                      <td>{money(invoice.amount)}</td>
                      <td>{money(invoice.isv)}</td>
                      <td className="font-black">{money(invoice.total)}</td>
                      <td>
                        <p className="font-mono text-xs">{invoice.cai}</p>
                        <p className="mt-1 text-xs text-slate-500">{invoice.correlative}</p>
                      </td>
                      <td>{shortDate(invoice.issuedAt)}</td>
                      <td><StatusBadge tone={statusTone(invoice.emailStatus)}>{invoice.emailStatus}</StatusBadge></td>
                      <td>{invoice.bacReference}</td>
                      <td className="no-print">
                        <div className="flex gap-2">
                          <ActionButton variant="secondary" onClick={() => downloadInvoice(invoice.number)}>PDF</ActionButton>
                          <ActionButton variant="secondary" onClick={() => resendInvoice(invoice.number, invoice.email)}>Reenviar</ActionButton>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </>
  );
}
