export default function Index() {
  return (
    <main style={{padding:16,fontFamily:'ui-sans-serif,system-ui',color:'#e6fffb',background:'#030b10',minHeight:'100vh'}}>
      <h1 style={{fontSize:18,marginBottom:8}}>Monday UI</h1>
      <p style={{opacity:.8}}>Denna app använder App Router (se <code>/app/page.js</code>), men Pages Router finns för API‑route (<code>/pages/api/token.ts</code>).</p>
    </main>
  );
}
