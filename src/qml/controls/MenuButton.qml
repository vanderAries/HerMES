import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15


Button{
    id: btnMenu
    // CUSTOM PROPERTIES
    property url btnIconSource: "../../images/svg_images/menu_icon.svg"
    property color btnColorDefault: "#1b1f22"
    property color btnColorMouseOver: "#2b3136"
    property color btnColorClicked: "#ce4500"

    QtObject{
        id: internal

        // MOUSE OVER AND CLICK CHANGE
        property var dynamicColor: if(btnMenu.down){
                                       btnMenu.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       btnMenu.hovered ? btnColorMouseOver : btnColorDefault
                                   }

    }

    implicitWidth: 70
    implicitHeight: 60

    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Image {
            id: iconBtn
            source: btnIconSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 25
            width: 25
            fillMode: Image.PreserveAspectFit
            visible: false
            antialiasing: false
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            antialiasing: false
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:4}
}
##^##*/
