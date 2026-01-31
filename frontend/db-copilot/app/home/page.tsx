"use client"

import { HomePage } from "../pages/HomePage"
import { AuthGuard } from "../components/AuthGuard"

export default function Home() {
    return (
        <AuthGuard>
            <HomePage />
        </AuthGuard>
    )
}