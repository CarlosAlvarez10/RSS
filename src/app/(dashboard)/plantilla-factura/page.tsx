'use client';

import * as React from 'react';
import { 
  Type, 
  ImageIcon, 
  Palette, 
  FileText, 
  Save, 
  Eye, 
  Undo,
  HelpCircle,
  Layout,
  Table as TableIcon,
  Upload,
  Download,
  Trash2
} from 'lucide-react';
import { cn } from '@/lib/utils';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

export default function InvoiceTemplatePage() {
  const [activeSection, setActiveSection] = React.useState('general');
  const [template, setTemplate] = React.useState({
    companyName: 'Mi Empresa S.A. de C.V.',
    rtn: '08019012345678',
    address: 'Col. Tepeyac, Edificio Comercial #402, Tegucigalpa, Honduras',
    phone: '+504 2233-4455',
    primaryColor: '#2563eb', // Blue-600
    headerText: 'FACTURA',
    legalText: 'La factura es beneficio de todos, ¡Exíjala!',
    showLogo: true,
    logoUrl: null as string | null,
  });

  const invoiceRef = React.useRef<HTMLDivElement>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setTemplate(prev => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setTemplate(prev => ({ ...prev, logoUrl: reader.result as string }));
      };
      reader.readAsDataURL(file);
    }
  };

  const removeLogo = () => {
    setTemplate(prev => ({ ...prev, logoUrl: null }));
  };

  const downloadPdf = async () => {
    if (!invoiceRef.current) return;
    
    // Create a copy of the content to strip out problematic things like the shadow
    const originalShadow = invoiceRef.current.style.boxShadow;
    const originalTransform = invoiceRef.current.style.transform;
    const originalTransition = invoiceRef.current.style.transition;
    
    // Temporary styling for capture
    invoiceRef.current.style.boxShadow = 'none';
    invoiceRef.current.style.transform = 'none';
    invoiceRef.current.style.transition = 'none';

    try {
      const canvas = await html2canvas(invoiceRef.current, {
        scale: 2, // 2 is usually enough and safer for memory
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        windowWidth: 1000, // Sufficient width for rendering
        onclone: (clonedDoc) => {
          // Cleanup clone for capture
          const capturedElement = clonedDoc.querySelector('[data-capture="invoice"]') as HTMLElement;
          if (capturedElement) {
            capturedElement.style.boxShadow = 'none';
            capturedElement.style.transform = 'none';
          }
          
          // html2canvas doesn't support CSS blur filters well
          const watermark = clonedDoc.querySelector('[data-watermark="logo"]') as HTMLElement;
          if (watermark) {
            watermark.style.filter = 'none';
            watermark.style.opacity = '0.08'; // Slightly more visible if blurred is gone
            const img = watermark.querySelector('img');
            if (img) img.style.filter = 'none';
          }
        }
      });
      
      const imgData = canvas.toDataURL('image/png');
      
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });
      
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
      
      // Use basic addImage call to avoid 'UNKNOWN' type errors
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight, undefined, 'FAST');
      pdf.save(`Factura_${template.companyName.replace(/\s+/g, '_')}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error al generar el PDF. El navegador podría estar bloqueando algunas funciones modernas.');
    } finally {
      // Restore original styling
      if (invoiceRef.current) {
        invoiceRef.current.style.boxShadow = originalShadow;
        invoiceRef.current.style.transform = originalTransform;
        invoiceRef.current.style.transition = originalTransition;
      }
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-20">
      <header className="flex flex-col md:flex-row justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Diseñador Profesional de Facturas</h1>
          <p className="text-sm text-slate-500">Configura la identidad visual de tus documentos fiscales Hondureños.</p>
        </div>
        <div className="flex gap-2">
           <button 
             onClick={downloadPdf}
             className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-bold hover:bg-emerald-700 shadow-md transition-all active:scale-95"
           >
              <Download className="w-4 h-4" />
              Descargar PDF
           </button>
           <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-medium hover:bg-slate-800 shadow-lg transition-all active:scale-95">
              <Save className="w-4 h-4" />
              Guardar Cambios
           </button>
        </div>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
        {/* Editor Sidebar */}
        <div className="xl:col-span-4 space-y-6">
           <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
              <div className="p-4 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
                 <h2 className="text-sm font-bold text-slate-900 uppercase tracking-widest">Panel de Control</h2>
                 <Layout className="w-4 h-4 text-slate-400" />
              </div>
              
              <div className="p-6 space-y-6">
                 {/* Navigation Inside Sidebar */}
                 <div className="flex gap-2 border-b border-slate-100 pb-4 mb-4 overflow-x-auto scrollbar-hide">
                    {[
                      { id: 'general', icon: Type, label: 'Identidad' },
                      { id: 'style', icon: Palette, label: 'Diseño' },
                      { id: 'legal', icon: FileText, label: 'Fiscal' },
                    ].map(tab => (
                      <button 
                        key={tab.id}
                        onClick={() => setActiveSection(tab.id)}
                        className={cn(
                          "px-4 py-2 rounded-xl text-xs font-black transition-all whitespace-nowrap uppercase tracking-wider",
                          activeSection === tab.id ? "bg-blue-600 text-white shadow-lg shadow-blue-200" : "text-slate-400 hover:bg-slate-100"
                        )}
                      >
                        {tab.label}
                      </button>
                    ))}
                 </div>

                 <div className="space-y-5">
                    {activeSection === 'general' && (
                      <>
                        <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Razón Social</label>
                           <input 
                             name="companyName" 
                             value={template.companyName} 
                             onChange={handleInputChange}
                             className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm font-semibold focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                           />
                        </div>
                        <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">RTN Empresa</label>
                           <input 
                             name="rtn" 
                             value={template.rtn} 
                             onChange={handleInputChange}
                             className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                           />
                        </div>
                        <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Dirección Fiscal</label>
                           <textarea 
                             name="address" 
                             value={template.address} 
                             onChange={handleInputChange}
                             rows={2}
                             className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none"
                           />
                        </div>
                         <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Contacto</label>
                           <input 
                             name="phone" 
                             value={template.phone} 
                             onChange={handleInputChange}
                             className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                           />
                        </div>
                      </>
                    )}

                    {activeSection === 'style' && (
                      <>
                        <div className="space-y-4">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Logotipo de Empresa</label>
                           <div className="relative group">
                              {template.logoUrl ? (
                                <div className="relative w-full aspect-video rounded-2xl border-2 border-dashed border-slate-200 overflow-hidden bg-slate-50 flex items-center justify-center p-4 transition-all hover:border-blue-300">
                                   <img src={template.logoUrl} alt="Logo preview" className="max-h-full object-contain" />
                                   <button 
                                     onClick={removeLogo}
                                     className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                                   >
                                      <Trash2 className="w-4 h-4" />
                                   </button>
                                </div>
                              ) : (
                                <label className="w-full aspect-video rounded-2xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center gap-3 cursor-pointer hover:bg-slate-50 hover:border-blue-300 transition-all text-slate-400 hover:text-blue-600">
                                   <Upload className="w-8 h-8" />
                                   <span className="text-xs font-bold uppercase tracking-widest">Subir Imagen</span>
                                   <input type="file" className="hidden" accept="image/*" onChange={handleImageUpload} />
                                </label>
                              )}
                           </div>
                           <p className="text-[10px] text-slate-400 text-center">Formatos sugeridos: PNG transparente o JPG (Max 2MB)</p>
                        </div>

                        <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Acento de Color</label>
                           <div className="flex gap-4 items-center p-1 bg-slate-50 rounded-2xl border border-slate-100">
                              <input 
                                type="color"
                                name="primaryColor" 
                                value={template.primaryColor} 
                                onChange={handleInputChange}
                                className="w-12 h-12 rounded-xl cursor-pointer bg-transparent border-0 shrink-0"
                              />
                              <input 
                                name="primaryColor" 
                                value={template.primaryColor} 
                                onChange={handleInputChange}
                                className="flex-1 bg-transparent text-sm font-mono font-bold text-slate-600 outline-none"
                              />
                           </div>
                        </div>
                         <div className="space-y-2">
                           <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Título del Documento</label>
                           <input 
                             name="headerText" 
                             value={template.headerText} 
                             onChange={handleInputChange}
                             className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm font-bold uppercase tracking-widest focus:ring-2 focus:ring-blue-500 outline-none transition-all"
                           />
                        </div>
                      </>
                    )}

                    {activeSection === 'legal' && (
                      <div className="space-y-4">
                         <div className="space-y-2">
                            <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Lema Fiscal (Honduras)</label>
                            <textarea 
                              name="legalText" 
                              value={template.legalText} 
                              onChange={handleInputChange}
                              rows={3}
                              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none font-medium leading-relaxed"
                            />
                         </div>
                         <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                            <h4 className="text-[10px] font-bold text-emerald-900 uppercase mb-1">Nota SAR</h4>
                            <p className="text-[10px] text-emerald-800 opacity-80 leading-snug">
                              &quot;La factura es beneficio de todos, ¡Exíjala!&quot; es obligatorio por ley en el pie de página de sus facturas según reglamento SAR.
                            </p>
                         </div>
                      </div>
                    )}
                 </div>
              </div>
           </div>

           <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-white relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-blue-600 rounded-full blur-3xl opacity-20 -mr-10 -mt-10" />
              <div className="relative flex gap-3 items-start">
                 <FileText className="w-6 h-6 text-blue-400 shrink-0" />
                 <div>
                    <h4 className="text-sm font-bold">Resumen de Plantilla</h4>
                    <ul className="text-[10px] text-slate-400 mt-2 space-y-1">
                       <li>• Formato: Autoincremental Fiscal</li>
                       <li>• Estilo: Moderno Corporativo</li>
                       <li>• Integración: Webhook Storeganise</li>
                    </ul>
                 </div>
              </div>
           </div>
        </div>

        {/* Live Preview Component */}
        <div className="xl:col-span-8">
           <div className="bg-slate-300 p-1 md:p-8 lg:p-12 rounded-[40px] min-h-[900px] flex items-center justify-center relative overflow-hidden group shadow-inner">
              <div className="absolute top-6 left-6 z-20">
                 <div className="flex bg-white/90 backdrop-blur-xl border border-white/50 rounded-2xl p-1 shadow-2xl">
                    <button className="px-4 py-2 text-[10px] font-black uppercase text-slate-600 bg-slate-50 rounded-xl flex items-center gap-2">
                       <Eye className="w-3 h-3" />
                       Vista Previa en Tiempo Real
                    </button>
                 </div>
              </div>

              {/* PDF Document Container */}
              <div 
                ref={invoiceRef}
                data-capture="invoice"
                className="w-full max-w-[620px] bg-white rounded-sm p-10 md:p-16 space-y-10 aspect-[1/1.414] transform transition-all duration-700 overflow-hidden relative"
                style={{ 
                  backgroundColor: '#ffffff'
                }}
              >
                 {/* Large Blurred Watermark Logo */}
                 {template.logoUrl && (
                   <div 
                     data-watermark="logo"
                     className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90%] h-[50%] opacity-[0.05] pointer-events-none select-none z-0"
                   >
                      <img 
                        src={template.logoUrl} 
                        className="w-full h-full object-contain grayscale scale-125 rotate-[-12deg]"
                        alt="Watermark" 
                        style={{ filter: 'blur(10px) grayscale(100%)' }}
                      />
                   </div>
                 )}

                 {/* Top Accent Bar */}
                 <div className="absolute top-0 right-0 left-0 h-2" style={{ backgroundColor: template.primaryColor }} />

                 <div className="flex justify-between items-start relative z-10">
                    <div className="space-y-4">
                       <div 
                         className="w-40 h-16 rounded-xl flex items-center justify-center overflow-hidden"
                         style={{ backgroundColor: '#f8fafc', border: '1px solid #f1f5f9' }}
                       >
                          {template.logoUrl ? (
                             <img src={template.logoUrl} className="max-h-full max-w-full object-contain p-2" alt="Logo" />
                          ) : (
                             <div className="flex flex-col items-center opacity-30" style={{ color: '#94a3b8' }}>
                                <ImageIcon className="w-5 h-5 mb-1" />
                                <span className="text-[8px] font-black">LOGOTIPO</span>
                             </div>
                          )}
                       </div>
                       <div className="space-y-1">
                          <h2 className="text-[14px] font-black uppercase tracking-tighter leading-none" style={{ color: '#0f172a' }}>{template.companyName}</h2>
                          <div className="text-[10px] leading-relaxed font-medium" style={{ color: '#64748b' }}>
                             <div className="flex items-center gap-1">
                                <span className="font-black" style={{ color: '#334155' }}>RTN:</span> {template.rtn}
                             </div>
                             <p className="max-w-[250px]">{template.address}</p>
                             <p><span className="font-black" style={{ color: '#334155' }}>TEL:</span> {template.phone}</p>
                          </div>
                       </div>
                    </div>
                    
                    <div className="text-right space-y-4">
                       <div>
                          <h3 
                            className="text-4xl font-black italic tracking-tighter leading-tight"
                            style={{ color: template.primaryColor }}
                          >
                            {template.headerText}
                          </h3>
                          <div className="flex flex-col items-end mt-1">
                             <span className="text-[11px] font-black uppercase tracking-widest px-2 py-1 rounded" style={{ backgroundColor: '#f8fafc', color: '#0f172a' }}>Original</span>
                             <span className="text-[11px] font-mono font-bold mt-1" style={{ color: '#94a3b8' }}>Nº 001-002-01-00004563</span>
                          </div>
                       </div>

                       <div className="p-4 rounded-2xl space-y-2 backdrop-blur-sm" style={{ backgroundColor: 'rgba(248, 250, 252, 0.5)', border: '1px solid #f1f5f9' }}>
                          <div className="text-right">
                             <p className="text-[8px] uppercase font-black tracking-[0.2em] mb-1" style={{ color: '#94a3b8' }}>C.A.I. AUTORIZADO</p>
                             <p className="text-[9px] font-mono font-bold leading-tight break-all max-w-[180px] ml-auto uppercase opacity-80" style={{ color: '#0f172a' }}>
                               87D56B-C3A124-B83321-7FFD12-9A4B12-1C
                             </p>
                          </div>
                       </div>
                    </div>
                 </div>

                 {/* Billing Info Grid */}
                 <div className="grid grid-cols-2 gap-12 text-[11px] py-8 relative z-10" style={{ borderTop: '2px solid rgba(15, 23, 42, 0.05)', borderBottom: '2px solid rgba(15, 23, 42, 0.05)' }}>
                    <div className="space-y-2">
                       <p className="text-[9px] font-black uppercase tracking-[0.2em]" style={{ color: '#94a3b8' }}>DATOS DEL CLIENTE</p>
                       <div className="space-y-1">
                          <p className="font-black text-[15px] tracking-tight" style={{ color: '#0f172a' }}>Distribuidora del Norte S.A.</p>
                          <p className="font-bold" style={{ color: '#475569' }}>RTN: 16011985123456</p>
                          <p className="font-medium italic" style={{ color: '#64748b' }}>San Pedro Sula, Cortés, Honduras</p>
                       </div>
                    </div>
                    <div className="space-y-3">
                       <div className="flex flex-col gap-1 text-right">
                          <p className="text-[9px] font-black uppercase tracking-[0.2em] mb-1" style={{ color: '#94a3b8' }}>DETALLE FISCAL</p>
                          <div className="flex justify-between items-center px-3 py-1.5 rounded-lg border" style={{ backgroundColor: '#f8fafc', borderColor: '#f1f5f9' }}>
                             <span className="font-bold uppercase text-[9px]" style={{ color: '#64748b' }}>FECHA EMISIÓN</span>
                             <span className="font-black" style={{ color: '#0f172a' }}>02 MAYO 2024</span>
                          </div>
                          <div className="flex justify-between items-center px-3 py-1.5 rounded-lg border mt-1" style={{ backgroundColor: '#f8fafc', borderColor: '#f1f5f9' }}>
                             <span className="font-bold uppercase text-[9px]" style={{ color: '#64748b' }}>CAJA/REGISTRO</span>
                             <span className="font-black" style={{ color: '#0f172a' }}>001-TP-02</span>
                          </div>
                       </div>
                    </div>
                 </div>

                 {/* Dynamic Items Table */}
                 <div className="space-y-[2px] relative z-10 rounded-2xl overflow-hidden border shadow-sm" style={{ borderColor: '#f1f5f9' }}>
                    <div 
                      className="grid grid-cols-12 p-4 text-white text-[10px] font-black uppercase tracking-[0.2em]" 
                      style={{ backgroundColor: template.primaryColor }}
                    >
                       <div className="col-span-8">Descripción Detallada del Servicio</div>
                       <div className="col-span-2 text-center">Cantidad</div>
                       <div className="col-span-2 text-right">Monto</div>
                    </div>
                    <div className="grid grid-cols-12 p-5 border-b text-[11px] bg-white transition-colors" style={{ borderBottomColor: '#f8fafc' }}>
                       <div className="col-span-8">
                          <p className="font-black tracking-tight leading-tight uppercase" style={{ color: '#0f172a' }}>Alquiler de Unidad Logística #402</p>
                          <p className="text-[9px] mt-1 font-medium italic uppercase tracking-wider" style={{ color: '#94a3b8' }}>Periodo: Mayo 2024 • Edificio Torre Norte</p>
                       </div>
                       <div className="col-span-2 text-center font-bold" style={{ color: '#64748b' }}>1.00</div>
                       <div className="col-span-2 text-right font-black italic tracking-tighter" style={{ color: '#0f172a' }}>L 12,450.00</div>
                    </div>
                     <div className="grid grid-cols-12 p-5 text-[11px]" style={{ backgroundColor: 'rgba(248, 250, 252, 0.4)' }}>
                       <div className="col-span-8 flex items-center gap-2">
                          <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: template.primaryColor }} />
                          <p className="font-medium uppercase tracking-tighter" style={{ color: '#64748b' }}>Consumo Eléctrico • Áreas Comunes</p>
                       </div>
                       <div className="col-span-2 text-center font-bold" style={{ color: '#cbd5e1' }}>1.00</div>
                       <div className="col-span-2 text-right font-medium italic opacity-70" style={{ color: '#64748b' }}>Incluido</div>
                    </div>
                 </div>

                 <div className="mt-12 flex justify-end relative z-10">
                    <div className="w-64 space-y-3">
                       <div className="space-y-1.5 px-4 font-bold" style={{ color: '#64748b' }}>
                          <div className="flex justify-between text-[11px] items-center">
                             <span className="uppercase tracking-tighter text-[9px]">Importe Gravado 15%</span>
                             <span style={{ color: '#0f172a' }}>L 10,826.09</span>
                          </div>
                          <div className="flex justify-between text-[11px] items-center border-b pb-2" style={{ borderBottomColor: '#f1f5f9' }}>
                             <span className="uppercase tracking-tighter text-[9px]">I.S.V. (Impuesto 15%)</span>
                             <span style={{ color: '#0f172a' }}>L 1,623.91</span>
                          </div>
                       </div>
                       <div 
                         className="flex justify-between items-center p-5 rounded-3xl border-2 text-[18px]" 
                         style={{ borderColor: template.primaryColor, backgroundColor: `${template.primaryColor}05` }}
                       >
                          <span className="font-black font-mono tracking-tighter italic uppercase text-[12px]" style={{ color: '#0f172a' }}>Total a Pagar</span>
                          <span className="font-black font-mono tracking-tighter" style={{ color: template.primaryColor }}>L 12,450.00</span>
                       </div>
                    </div>
                 </div>

                 {/* Fiscal Bottom Section */}
                 <div className="mt-auto pt-12 text-[9px] text-center uppercase tracking-[0.2em] border-t space-y-4 relative z-10 font-bold" style={{ borderTopColor: '#f1f5f9', color: '#94a3b8' }}>
                    <p 
                      className="text-[12px] italic tracking-tight mb-2 opacity-90" 
                      style={{ color: template.primaryColor }}
                    >
                      &quot;{template.legalText}&quot;
                    </p>
                    <div className="grid grid-cols-2 gap-4 text-[8px] p-4 rounded-2xl border" style={{ backgroundColor: 'rgba(248, 250, 252, 0.5)', borderColor: '#f1f5f9' }}>
                       <div className="text-left space-y-1 border-r" style={{ borderRightColor: '#e2e8f0' }}>
                          <p className="font-black" style={{ color: '#64748b' }}>Rango Autorizado:</p>
                          <p className="opacity-70 font-mono">001-002-01-00004501 AL 001-002-01-00005500</p>
                       </div>
                       <div className="text-right space-y-1">
                          <p className="font-black" style={{ color: '#64748b' }}>Fecha Límite de Emisión:</p>
                          <p className="font-black" style={{ color: template.primaryColor }}>15 DE ENERO, 2025</p>
                       </div>
                    </div>
                    <p className="text-[7px] font-medium" style={{ color: '#cbd5e1' }}>Este documento es una impresión representativa de un documento fiscal digital • Sistema Integrado SAR-Connect</p>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}
