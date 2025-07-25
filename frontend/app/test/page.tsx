export default function TestPage() {
  return (
    <div style={{
      padding: '20px',
      backgroundColor: 'red',
      color: 'white',
      fontSize: '24px',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1>TEST PAGE - If you see this, JavaScript is working!</h1>
      <p>This page uses inline styles to test if the issue is CSS-related.</p>
      <p>Background should be red, text should be white.</p>
      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: 'blue' }}>
        This is a blue box inside the red container.
      </div>
    </div>
  )
}