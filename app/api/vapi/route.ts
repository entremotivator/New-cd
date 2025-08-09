import { NextResponse } from "next/server"

export async function GET() {
  const vapiApiKey = process.env.VAPI_API_KEY

  if (!vapiApiKey) {
    return NextResponse.json({ error: "VAPI_API_KEY not configured" }, { status: 500 })
  }

  // In a real application, you would use this API key to interact with the VAPI.ai API
  // For example, to create a call, retrieve assistant details, etc.
  // This is a placeholder to demonstrate access to the environment variable.

  return NextResponse.json({
    message: "VAPI API key accessed successfully (server-side)",
    // Do NOT expose the actual API key to the client in a real application.
    // This is for demonstration purposes only.
    apiKeyPreview: vapiApiKey.substring(0, 5) + "..." + vapiApiKey.substring(vapiApiKey.length - 5),
  })
}

export async function POST(request: Request) {
  const vapiApiKey = process.env.VAPI_API_KEY

  if (!vapiApiKey) {
    return NextResponse.json({ error: "VAPI_API_KEY not configured" }, { status: 500 })
  }

  try {
    const body = await request.json()
    // Process the request body, e.g., initiate a call via VAPI.ai
    console.log("Received VAPI request:", body)

    // Example: Call VAPI.ai API (replace with actual VAPI.ai SDK/fetch calls)
    // const response = await fetch('https://api.vapi.ai/call', {
    //   method: 'POST',
    //   headers: {
    //     'Authorization': `Bearer ${vapiApiKey}`,
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify(body),
    // });
    // const data = await response.json();
    // return NextResponse.json(data, { status: response.status });

    return NextResponse.json({ message: "VAPI request processed (placeholder)" })
  } catch (error) {
    console.error("Error processing VAPI request:", error)
    return NextResponse.json({ error: "Failed to process VAPI request" }, { status: 500 })
  }
}
