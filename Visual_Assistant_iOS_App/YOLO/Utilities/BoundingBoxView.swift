//  BoundingBoxView.swift
//  This file defines the BoundingBoxView class which is responsible for visualising bounding boxes
//  and displaying associated labels and confidence scores for object detection results.
//  The code utilises UIKit and Foundation to create and manage CALayer objects for drawing and text display.

import Foundation  // Provides fundamental data types and utilities.
import UIKit      // Provides the UI elements and graphics functionalities needed for drawing.

// MARK: - BoundingBoxView Class

/// Manages the visualisation of bounding boxes and associated labels for object detection results.
class BoundingBoxView {
    
    /// The CAShapeLayer that is used to draw the bounding box around a detected object.
    let shapeLayer: CAShapeLayer

    /// The CATextLayer that is used to display the label and confidence score for the detected object.
    let textLayer: CATextLayer

    // MARK: - Initialisation

    /// Initialises a new BoundingBoxView with pre-configured shape and text layers.
    ///
    /// The initialiser sets up the shapeLayer to have no fill colour, a fixed stroke width, and
    /// remains hidden until explicitly displayed. The textLayer is also configured for clear display,
    /// including setting its scale for Retina displays, font size, and font type.
    init() {
        // Initialise the shapeLayer for drawing the bounding box.
        shapeLayer = CAShapeLayer()
        shapeLayer.fillColor = UIColor.clear.cgColor  // Set fill colour to clear as only the outline is required.
        shapeLayer.lineWidth = 4  // Define the stroke width of the bounding box.
        shapeLayer.isHidden = true  // Initially hidden until the bounding box is required.

        // Initialise the textLayer for displaying the label and confidence score.
        textLayer = CATextLayer()
        textLayer.isHidden = true  // Initially hidden until the label needs to be shown.
        textLayer.contentsScale = UIScreen.main.scale  // Ensures that the text is rendered sharply on Retina displays.
        textLayer.fontSize = 14  // Set the font size for the text label.
        textLayer.font = UIFont(name: "Avenir", size: textLayer.fontSize)  // Apply the Avenir font to the text.
        textLayer.alignmentMode = .center  // Centre-align the text within the layer.
    }

    // MARK: - Layer Management

    /// Adds the bounding box and text layers to a specified parent CALayer.
    ///
    /// - Parameter parent: The CALayer to which the bounding box (shapeLayer) and the label (textLayer) will be added.
    /// This method is typically called when the view hierarchy is being set up.
    func addToLayer(_ parent: CALayer) {
        // Add the shapeLayer and textLayer as sublayers of the provided parent layer.
        parent.addSublayer(shapeLayer)
        parent.addSublayer(textLayer)
    }

    // MARK: - Display Methods

    /// Displays the bounding box and label with specified properties.
    ///
    /// - Parameters:
    ///   - frame: A CGRect that defines the size and position of the bounding box.
    ///   - label: The text label to be displayed above the bounding box.
    ///   - color: The UIColor used for the bounding box stroke and label background.
    ///   - alpha: The opacity level for both the bounding box and the label background.
    ///
    /// This method configures both the shapeLayer and textLayer for immediate visual feedback by disabling
    /// implicit animations, setting up the graphical path, and calculating the appropriate size and position for the text.
    func show(frame: CGRect, label: String, color: UIColor, alpha: CGFloat) {
        // Disable implicit animations to ensure that updates are applied immediately.
        CATransaction.setDisableActions(true)

        // Create a UIBezierPath representing a rounded rectangle to be used as the bounding box.
        let path = UIBezierPath(roundedRect: frame, cornerRadius: 6.0)
        shapeLayer.path = path.cgPath  // Set the path for the shapeLayer.
        // Set the stroke colour of the bounding box, adjusting for the specified opacity.
        shapeLayer.strokeColor = color.withAlphaComponent(alpha).cgColor
        shapeLayer.isHidden = false  // Make the shapeLayer visible.

        // Configure the textLayer with the label information.
        textLayer.string = label  // Set the displayed text.
        textLayer.backgroundColor = color.withAlphaComponent(alpha).cgColor  // Set the background colour with opacity.
        textLayer.isHidden = false  // Ensure the textLayer is visible.
        // Set the text colour to white with the same opacity.
        textLayer.foregroundColor = UIColor.white.withAlphaComponent(alpha).cgColor

        // Calculate the size of the text based on the provided label and font attributes.
        let attributes = [NSAttributedString.Key.font: textLayer.font as Any]
        let textRect = label.boundingRect(with: CGSize(width: 400, height: 100),
                                          options: .truncatesLastVisibleLine,
                                          attributes: attributes, context: nil)
        // Add padding to the text width to ensure adequate spacing.
        let textSize = CGSize(width: textRect.width + 12, height: textRect.height)
        // Position the text layer slightly above the bounding box.
        let textOrigin = CGPoint(x: frame.origin.x - 2, y: frame.origin.y - textSize.height - 2)
        textLayer.frame = CGRect(origin: textOrigin, size: textSize)
    }

    // MARK: - Hide Methods

    /// Hides both the bounding box and the text label.
    ///
    /// This method simply sets the `isHidden` property of both layers to true, effectively removing them from view.
    func hide() {
        shapeLayer.isHidden = true  // Hide the shapeLayer.
        textLayer.isHidden = true   // Hide the textLayer.
    }
}
