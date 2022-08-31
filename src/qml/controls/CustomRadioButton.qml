import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

    RadioButton {
        id: radioButton

        // Custom Properties
        property string setText: "Automatic"
        property color colorTextActive: "#ffffff"
        property color colorTextDisabled: "#808a95"
        property color colorActive: "#25282b"
        property color colorDisabled: "#808a95"


        text: qsTr("RadioButton")
        checkable: true
        checked: true
        contentItem: Text {
            height: 20
            color: checkable ? colorTextActive : colorTextDisabled
            text: setText
            verticalAlignment: Text.AlignVCenter
            leftPadding: radioButton.indicator.width + radioButton.spacing
            font: radioButton.font
        }
        indicator: Rectangle {
            x: radioButton.leftPadding
            y: parent.height / 2 - height / 2
            radius: 10
            border.color: checkable ? colorActive : colorDisabled
            Rectangle {
                x: 3
                y: 3
                width: 14
                height: 14
                visible: radioButton.checked
                color: checkable ? colorActive : colorDisabled
                radius: 8
            }
            implicitHeight: 20
            implicitWidth: 20
        }
    }

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:3;height:32;width:88}
}
##^##*/
