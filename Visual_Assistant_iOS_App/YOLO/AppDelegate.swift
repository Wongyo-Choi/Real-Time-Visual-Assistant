//  AppDelegate.swift
//  This file contains the AppDelegate class, which serves as the entry point for the application.
//  It is responsible for setting global app configurations upon launch and managing essential app-wide behaviours.
//  Additionally, an extension to CALayer is provided to facilitate screenshot functionality.

import UIKit  // Import the UIKit framework to manage the app’s user interface and life-cycle events.

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    // The main window of the application where the view hierarchy is rendered.
    var window: UIWindow?

    /// Called when the app has finished launching.
    ///
    /// This method is utilised to perform final initialisations before the app is presented to the user.
    /// It disables auto-lock, enables battery monitoring, and stores essential information such as
    /// the app version, build number, and device UUID in UserDefaults for future reference.
    ///
    /// - Parameters:
    ///   - application: The singleton app object.
    ///   - launchOptions: A dictionary indicating the reason the app was launched, if any.
    /// - Returns: A Boolean value indicating whether the app successfully handled the launch.
    func application(_ application: UIApplication,
                     didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Disable auto-lock to ensure that the app remains active during use.
        UIApplication.shared.isIdleTimerDisabled = true

        // Enable battery monitoring to track the device's battery status.
        UIDevice.current.isBatteryMonitoringEnabled = true

        // Retrieve the app's version and build number from the bundle's info dictionary.
        // These details are then stored in UserDefaults for debugging or informational purposes.
        if let appVersion = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String,
           let buildVersion = Bundle.main.infoDictionary?["CFBundleVersion"] as? String {
            // Save the app version in the format "version (build)".
            UserDefaults.standard.set("\(appVersion) (\(buildVersion))", forKey: "app_version")
        }

        // Retrieve the device's unique identifier (UUID) and store it in UserDefaults.
        if let uuid = UIDevice.current.identifierForVendor?.uuidString {
            UserDefaults.standard.set(uuid, forKey: "uuid")
        }

        // Synchronise UserDefaults to ensure that all changes are immediately written.
        UserDefaults.standard.synchronize()
        return true  // Return true to indicate that the app has launched successfully.
    }
}

/// Extension to CALayer providing screenshot functionality.
///
/// This extension adds a computed property that captures the current visual content of the CALayer as a UIImage.
/// It utilises UIKit's graphics context capabilities to render the layer's content into an image.
extension CALayer {
    /// Captures a screenshot of the current appearance of the CALayer.
    ///
    /// - Returns: An optional UIImage representing the screenshot, or nil if the image capture fails.
    var screenShot: UIImage? {
        // Begin a new image context with the layer's size and the device's screen scale for optimal resolution.
        UIGraphicsBeginImageContextWithOptions(frame.size, false, UIScreen.main.scale)
        // Ensure that the image context is ended when the method exits, regardless of success or failure.
        defer { UIGraphicsEndImageContext() }
        // Attempt to obtain the current graphics context.
        if let context = UIGraphicsGetCurrentContext() {
            // Render the layer's contents into the current graphics context.
            render(in: context)
            // Retrieve and return the image from the current image context.
            return UIGraphicsGetImageFromCurrentImageContext()
        }
        // Return nil if the graphics context is unavailable.
        return nil
    }
}
