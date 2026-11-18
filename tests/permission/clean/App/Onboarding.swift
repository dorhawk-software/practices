import SwiftUI
import FamilyControls

// The page before iOS asks: the reason, then Continue. Never "Allow …".
struct AccessPage: View {
    var body: some View {
        VStack {
            Text("Acme needs Screen Time access to set your limits.")
            Button("Continue") {
                Task { try? await AuthorizationCenter.shared.requestAuthorization(for: .individual) }
            }
            Button("Not now") {}
        }
    }
}

// A step in a guide names the switch in Settings; no prompt follows it.
// practices-allow permission: names the Settings switch
let settingsStep = "Allow notifications"
let guideStep = "Turn on a Screen Time passcode"
