//  ThresholdProvider.swift
//  This file defines the ThresholdProvider class which conforms to the MLFeatureProvider protocol.
//  It supplies custom IoU and confidence thresholds for adjusting model predictions.
//  All comments and documentation are written in British English for academic clarity.

import CoreML  // Import the CoreML framework to utilise machine learning functionalities.

/// Provides custom IoU and confidence thresholds for adjusting model predictions.
class ThresholdProvider: MLFeatureProvider {

    /// Dictionary to store IoU and confidence thresholds as MLFeatureValue objects.
    /// Each threshold is associated with a specific feature name.
    var values: [String: MLFeatureValue]

    /// The set of feature names provided by this provider.
    /// This computed property extracts and returns the keys from the 'values' dictionary as a Set.
    var featureNames: Set<String> {
        // Convert the dictionary keys into a Set and return.
        return Set(values.keys)
    }

    /// Initialiser for the ThresholdProvider class.
    /// - Parameters:
    ///   - iouThreshold: The IoU threshold for determining object overlap. Defaults to 0.5.
    ///   - confidenceThreshold: The minimum confidence required for a detection to be considered valid. Defaults to 0.5.
    ///
    /// This initialiser converts the provided Double thresholds into MLFeatureValue objects
    /// and stores them within the 'values' dictionary for later access.
    init(iouThreshold: Double = 0.5, confidenceThreshold: Double = 0.5) {
        values = [
            // Store the IoU threshold using the key "iouThreshold".
            "iouThreshold": MLFeatureValue(double: iouThreshold),
            // Store the confidence threshold using the key "confidenceThreshold".
            "confidenceThreshold": MLFeatureValue(double: confidenceThreshold)
        ]
    }

    /// Returns the MLFeatureValue corresponding to the specified feature name.
    /// - Parameter featureName: The name of the feature whose value is requested.
    /// - Returns: The MLFeatureValue object corresponding to the feature name, or nil if the feature is not found.
    ///
    /// This method provides access to the stored threshold values via their associated feature names.
    func featureValue(for featureName: String) -> MLFeatureValue? {
        // Retrieve the MLFeatureValue from the dictionary using the provided feature name.
        return values[featureName]
    }
}
