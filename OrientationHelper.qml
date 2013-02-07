/*
 * Copyright 2013 Canonical Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; version 3.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.0
import QtSensors 5.0

QtObject {
    property Item root

    /* What's the physical default orientation of the device (e.g. most phones are portait
       and most tablets are landscape) */
    property string naturalOrientation: root.height < root.width ? "landscape" : "portrait"

    /* Is the device currently rotated to be in lanscape orientation ? */
    property bool isLandscape: (naturalOrientation == "landscape" &&
                                (orientationSensor.lastNonFlatReading == OrientationReading.TopUp ||
                                 orientationSensor.lastNonFlatReading == OrientationReading.TopDown))
                               ||
                               (naturalOrientation == "portrait" &&
                                (orientationSensor.lastNonFlatReading == OrientationReading.LeftUp ||
                                 orientationSensor.lastNonFlatReading == OrientationReading.RightUp))

    /* Is the device currently rotated upside down ? */
    property bool isInverted: orientationSensor.lastNonFlatReading == OrientationReading.RightUp ||
                              orientationSensor.lastNonFlatReading == OrientationReading.TopDown

    /* The rotation angle in 90 degrees increments with respect to the device being in its
       default position */
    property int rotationAngle: 0

    property OrientationSensor sensor: OrientationSensor {
        id: orientationSensor
        active: true

        /* Last measurement taken while the device wasn't face up or face down */
        property int lastNonFlatReading: OrientationReading.TopUp

        onReadingChanged: {
            if (reading.orientation == OrientationReading.LeftUp) {
                rotationAngle = 270
                lastNonFlatReading = reading.orientation;
            }
            else if (reading.orientation == OrientationReading.RightUp) {
                rotationAngle = 90
                lastNonFlatReading = reading.orientation;
            }
            else if (reading.orientation == OrientationReading.TopUp) {
                rotationAngle = 0
                lastNonFlatReading = reading.orientation;
            }
            else if (reading.orientation == OrientationReading.TopDown) {
                rotationAngle = 180
                lastNonFlatReading = reading.orientation;
            }
        }
    }
}
