import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

TextField {
    id: textField

    // Custom Properties
    property color colorDefault: "#282c34"
    property color colorOnFocus: "#242831"
    property color colorMouseOver: "#2B2F38"
    property color colorText: "#ffffff"

    QtObject{
        id: internal

        property var dynamicColor: if(textField.focus){
                                        textField.hovered ? colorOnFocus : colorDefault
                                   }else{
                                       textField.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 100
    implicitHeight: 30
    placeholderText: qsTr("Type something")
    color: colorText
    background: Rectangle {
        color: internal.dynamicColor
        radius: 10
    }

    selectByMouse: true
    selectedTextColor: colorText
    selectionColor: "#ce6835"
    placeholderTextColor: "#81848c"
}

