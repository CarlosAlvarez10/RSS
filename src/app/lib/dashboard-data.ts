export type PaymentStatus =
  | "PENDING"
  | "APPROVED"
  | "REJECTED"
  | "FAILED"
  | "CANCELLED"
  | "REFUNDED";

export type EmailStatus = "ENVIADA" | "PENDIENTE" | "FALLIDA";
export type AlertLevel = "INFO" | "WARNING" | "CRITICAL";
export type CaiStatus = "ACTIVO" | "INACTIVO" | "VENCIDO" | "AGOTADO";

export type Invoice = {
  id: string;
  number: string;
  client: string;
  rtn: string;
  email: string;
  amount: number;
  isv: number;
  total: number;
  cai: string;
  correlative: string;
  issuedAt: string;
  emailStatus: EmailStatus;
  bacReference: string;
  paymentId: string;
};

export type BacPayment = {
  id: string;
  client: string;
  email: string;
  amount: number;
  status: PaymentStatus;
  bacReference: string;
  transactionId: string;
  paidAt: string;
  invoiceNumber?: string;
  bankResponse: string;
  confirmed: boolean;
  error?: string;
};

export type CaiRange = {
  id: string;
  cai: string;
  initial: number;
  final: number;
  current: number;
  limitDate: string;
  status: CaiStatus;
  branch: string;
  point: string;
  documentType: string;
};

export type StoreganiseEvent = {
  id: string;
  event: string;
  status: "RECIBIDO" | "PROCESADO" | "ERROR" | "REINTENTO";
  receivedAt: string;
  payloadRef: string;
  retries: number;
  message: string;
};

export type SystemAlert = {
  id: string;
  level: AlertLevel;
  title: string;
  message: string;
  area: "CAI" | "BAC" | "EMAIL" | "STOREGANISE" | "PDF";
  createdAt: string;
  resolved: boolean;
};

export const money = (value: number) =>
  new Intl.NumberFormat("es-HN", {
    style: "currency",
    currency: "HNL",
    minimumFractionDigits: 2,
  }).format(value);

export const shortDate = (value: string) =>
  new Intl.DateTimeFormat("es-HN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));

export const invoices: Invoice[] = [
  {
    id: "fac-001",
    number: "001-002-01-00004563",
    client: "Distribuidora del Norte",
    rtn: "16011985123456",
    email: "contabilidad@dnorte.hn",
    amount: 10826.09,
    isv: 1623.91,
    total: 12450,
    cai: "87D56B-C3A124-B83321-7FFD12-9A4B12-1C",
    correlative: "00004563",
    issuedAt: "2026-05-02T09:18:00-06:00",
    emailStatus: "ENVIADA",
    bacReference: "BAC-8822",
    paymentId: "pay-001",
  },
  {
    id: "fac-002",
    number: "001-002-01-00004564",
    client: "Roatan Dive Center",
    rtn: "05011990004567",
    email: "admin@roatandive.hn",
    amount: 7565.22,
    isv: 1134.78,
    total: 8700,
    cai: "87D56B-C3A124-B83321-7FFD12-9A4B12-1C",
    correlative: "00004564",
    issuedAt: "2026-05-02T11:42:00-06:00",
    emailStatus: "PENDIENTE",
    bacReference: "BAC-8831",
    paymentId: "pay-002",
  },
  {
    id: "fac-003",
    number: "001-002-01-00004565",
    client: "Hotel Coral Bay",
    rtn: "08019999112233",
    email: "finanzas@coralbay.hn",
    amount: 14260.87,
    isv: 2139.13,
    total: 16400,
    cai: "87D56B-C3A124-B83321-7FFD12-9A4B12-1C",
    correlative: "00004565",
    issuedAt: "2026-04-30T15:25:00-06:00",
    emailStatus: "ENVIADA",
    bacReference: "BAC-8709",
    paymentId: "pay-003",
  },
  {
    id: "fac-004",
    number: "001-002-01-00004566",
    client: "Constructora Insular",
    rtn: "11011988009876",
    email: "pagos@insular.hn",
    amount: 5217.39,
    isv: 782.61,
    total: 6000,
    cai: "87D56B-C3A124-B83321-7FFD12-9A4B12-1C",
    correlative: "00004566",
    issuedAt: "2026-04-28T10:05:00-06:00",
    emailStatus: "FALLIDA",
    bacReference: "BAC-8660",
    paymentId: "pay-004",
  },
];

export const payments: BacPayment[] = [
  {
    id: "pay-001",
    client: "Distribuidora del Norte",
    email: "contabilidad@dnorte.hn",
    amount: 12450,
    status: "APPROVED",
    bacReference: "BAC-8822",
    transactionId: "TX-905551",
    paidAt: "2026-05-02T09:16:00-06:00",
    invoiceNumber: "001-002-01-00004563",
    bankResponse: "Aprobado por BAC Credomatic",
    confirmed: true,
  },
  {
    id: "pay-002",
    client: "Roatan Dive Center",
    email: "admin@roatandive.hn",
    amount: 8700,
    status: "PENDING",
    bacReference: "BAC-8831",
    transactionId: "TX-905590",
    paidAt: "2026-05-02T11:39:00-06:00",
    invoiceNumber: "001-002-01-00004564",
    bankResponse: "Pendiente de confirmación del banco",
    confirmed: false,
  },
  {
    id: "pay-003",
    client: "Hotel Coral Bay",
    email: "finanzas@coralbay.hn",
    amount: 16400,
    status: "APPROVED",
    bacReference: "BAC-8709",
    transactionId: "TX-904870",
    paidAt: "2026-04-30T15:20:00-06:00",
    invoiceNumber: "001-002-01-00004565",
    bankResponse: "Aprobado por BAC Credomatic",
    confirmed: true,
  },
  {
    id: "pay-004",
    client: "Constructora Insular",
    email: "pagos@insular.hn",
    amount: 6000,
    status: "FAILED",
    bacReference: "BAC-8660",
    transactionId: "TX-904201",
    paidAt: "2026-04-28T09:58:00-06:00",
    invoiceNumber: "001-002-01-00004566",
    bankResponse: "Error de comunicación con BAC",
    confirmed: false,
    error: "Timeout consultando estado final de la transacción.",
  },
  {
    id: "pay-005",
    client: "Island Market",
    email: "caja@islandmarket.hn",
    amount: 3500,
    status: "REJECTED",
    bacReference: "BAC-8644",
    transactionId: "TX-904188",
    paidAt: "2026-04-27T12:01:00-06:00",
    bankResponse: "Transacción rechazada por el emisor",
    confirmed: false,
    error: "Fondos insuficientes o autorización denegada.",
  },
];

export const caiRanges: CaiRange[] = [
  {
    id: "cai-001",
    cai: "87D56B-C3A124-B83321-7FFD12-9A4B12-1C",
    initial: 4501,
    final: 5500,
    current: 4566,
    limitDate: "2026-06-15",
    status: "ACTIVO",
    branch: "001",
    point: "002",
    documentType: "01",
  },
  {
    id: "cai-002",
    cai: "91F22A-B991C0-4332AA-8100EE-5A8891-3F",
    initial: 3001,
    final: 4500,
    current: 4500,
    limitDate: "2026-03-30",
    status: "AGOTADO",
    branch: "001",
    point: "002",
    documentType: "01",
  },
];

export const storeganiseEvents: StoreganiseEvent[] = [
  {
    id: "sg-001",
    event: "unitRental.invoice.created",
    status: "PROCESADO",
    receivedAt: "2026-05-02T09:12:00-06:00",
    payloadRef: "SG-INV-8822",
    retries: 0,
    message: "Factura de alquiler recibida y vinculada a pago BAC.",
  },
  {
    id: "sg-002",
    event: "invoice.payments.updated",
    status: "PROCESADO",
    receivedAt: "2026-05-02T11:37:00-06:00",
    payloadRef: "SG-INV-8831",
    retries: 0,
    message: "Pago actualizado desde Storeganise.",
  },
  {
    id: "sg-003",
    event: "user.billing.updated",
    status: "ERROR",
    receivedAt: "2026-05-01T16:44:00-06:00",
    payloadRef: "SG-USER-1920",
    retries: 2,
    message: "RTN incompleto en datos de facturación.",
  },
  {
    id: "sg-004",
    event: "addon.dailyEvent.started",
    status: "RECIBIDO",
    receivedAt: "2026-05-02T06:00:00-06:00",
    payloadRef: "SG-DAILY-0502",
    retries: 0,
    message: "Proceso diario recibido.",
  },
];

export const alerts: SystemAlert[] = [
  {
    id: "al-001",
    level: "WARNING",
    title: "CAI próximo a vencer",
    message: "El CAI activo vence el 15 de junio de 2026.",
    area: "CAI",
    createdAt: "2026-05-02T08:00:00-06:00",
    resolved: false,
  },
  {
    id: "al-002",
    level: "CRITICAL",
    title: "Factura no enviada por correo",
    message: "La factura 001-002-01-00004566 falló al enviarse.",
    area: "EMAIL",
    createdAt: "2026-04-28T10:08:00-06:00",
    resolved: false,
  },
  {
    id: "al-003",
    level: "WARNING",
    title: "Pago BAC pendiente",
    message: "BAC-8831 aún no confirma estado final.",
    area: "BAC",
    createdAt: "2026-05-02T11:43:00-06:00",
    resolved: false,
  },
  {
    id: "al-004",
    level: "INFO",
    title: "Storeganise sincronizado",
    message: "Última sincronización procesada correctamente.",
    area: "STOREGANISE",
    createdAt: "2026-05-02T11:45:00-06:00",
    resolved: true,
  },
];

export const activeCai = caiRanges.find((range) => range.status === "ACTIVO");

export function getAvailableCorrelatives(range = activeCai) {
  if (!range) return 0;
  return Math.max(range.final - range.current, 0);
}

export function canGenerateInvoice(range = activeCai) {
  if (!range) return { ok: false, reason: "No hay CAI activo." };
  if (range.status !== "ACTIVO") return { ok: false, reason: "El CAI no está activo." };
  if (new Date(range.limitDate) < new Date()) return { ok: false, reason: "El CAI está vencido." };
  if (getAvailableCorrelatives(range) <= 0) return { ok: false, reason: "El rango está agotado." };
  return { ok: true, reason: "El sistema puede generar facturas." };
}

export const overview = {
  billedToday: invoices
    .filter((invoice) => invoice.issuedAt.startsWith("2026-05-02"))
    .reduce((sum, invoice) => sum + invoice.total, 0),
  billedMonth: invoices
    .filter((invoice) => invoice.issuedAt.startsWith("2026-05"))
    .reduce((sum, invoice) => sum + invoice.total, 0),
  approvedPayments: payments.filter((payment) => payment.status === "APPROVED").length,
  pendingPayments: payments.filter((payment) => payment.status === "PENDING").length,
  generatedInvoices: invoices.length,
  sentInvoices: invoices.filter((invoice) => invoice.emailStatus === "ENVIADA").length,
  criticalAlerts: alerts.filter((alert) => alert.level === "CRITICAL" && !alert.resolved).length,
  storeganiseStatus: storeganiseEvents.some((event) => event.status === "ERROR")
    ? "CON ERRORES"
    : "OPERATIVO",
};
