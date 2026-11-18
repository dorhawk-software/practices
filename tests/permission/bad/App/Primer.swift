import SwiftUI
import UserNotifications

struct Primer: View {
    var body: some View {
        Button("Allow") {
            Task { _ = try? await UNUserNotificationCenter.current().requestAuthorization(options: [.alert]) }
        }
        // practices-allow permission: guide
        Text("Enable location")
    }
}
