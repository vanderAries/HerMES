import QtQuick 2.15
import QtQuick.Controls 2.15

Item {

    Rectangle {
        id: rectangle
        color: "#2d3439"
        anchors.fill: parent

        Label {
            id: label
            x: 319
            y: 174
            width: 149
            height: 41
            color: "#ffffff"
            text: qsTr("Settings Page")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pointSize: 16
        }
    }

}

/*##^##
Designer {
    D{i:0;formeditorZoom:1.1}D{i:1}
}
##^##*/
