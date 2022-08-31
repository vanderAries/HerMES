import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

SpinBox {
    id: control

    // Custom Properties
    property color colorDefault: "#66707b"
    property color colorMouseOver: "#b46843"
    property color colorPressed: "#ce4500"


    QtObject{
        id: internal

        property var dynamicColorDown: if(control.down.pressed){
                                       control.down.pressed ? colorPressed : colorDefault
                                   }else{
                                       control.down.hovered ? colorMouseOver : colorDefault
                                   }
        property var dynamicColorUp: if(control.up.pressed){
                                       control.up.pressed ? colorPressed : colorDefault
                                   }else{
                                       control.up.hovered ? colorMouseOver : colorDefault
                                   }
    }

    value: 50
    editable: true

    contentItem: TextInput {
        z: 2
        text: control.textFromValue(control.value, control.locale)

        font: control.font
        color: enabled ? "#ffffff" : "#a6abae"
        selectionColor: "#25282b"
        selectedTextColor: "#ffffff"
        horizontalAlignment: Qt.AlignHCenter
        verticalAlignment: Qt.AlignVCenter

        readOnly: !control.editable
        validator: control.validator
        inputMethodHints: Qt.ImhFormattedNumbersOnly
    }

    up.indicator: Rectangle {
        x: control.mirrored ? 0 : parent.width - width
        height: parent.height
        implicitWidth: 40
        implicitHeight: 40
        radius: 10
        color: internal.dynamicColorUp

        Text {
            color: enabled ? "#ffffff" : "#a6abae"
            text: "+"
            anchors.fill: parent
            font.pixelSize: 25
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            lineHeight: 0.5
            lineHeightMode: Text.ProportionalHeight
        }
    }

    down.indicator: Rectangle {
        x: control.mirrored ? parent.width - width : 0
        height: parent.height
        implicitWidth: 40
        implicitHeight: 40
        radius: 10
        color: internal.dynamicColorDown

        Text {
            color: enabled ? "#ffffff" : "#a6abae"
            text: "-"
            anchors.fill: parent
            font.pixelSize: 40
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            lineHeight: 1
            lineHeightMode: Text.ProportionalHeight
            minimumPixelSize: 12
        }
    }

    background: Rectangle {
        color: "#66707b"
        implicitWidth: 140
        radius: 10
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.66;height:40;width:200}
}
##^##*/
