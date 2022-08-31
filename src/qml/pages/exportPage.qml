import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.15
import "../controls"

Item {

    Rectangle {
        id: rectangle
        color: "#2d3439"
        anchors.fill: parent

        FileDialog{
            id: fileExport2D
            title: "Save data file"
            selectMultiple: false
            nameFilters: ["JSON (*.json)"]
            selectExisting: false
            onAccepted: {
                backend.exportTo2D(fileExport2D.fileUrl)
            }
        }

        FileDialog{
            id: fileExport3D
            title: "Save data file"
            selectMultiple: false
            nameFilters: ["JSON (*.json)"]
            selectExisting: false
            onAccepted: {
                backend.exportTo3D(fileExport3D.fileUrl)
            }
        }

        FileDialog{
            id: resultsExport
            title: "Save data file"
            selectMultiple: false
            nameFilters: ["JSON (*.json)"]
            selectExisting: false
            onAccepted: {
                backend.resultsExport(resultsExport.fileUrl)
            }
        }


        ColumnLayout {
            id: columnLayout
            x: 0
            width: 250
            height: 240
            anchors.top: parent.top
            anchors.topMargin: 40

            Text {
                id: text1
                color: "#ffffff"
                text: qsTr("Geometry export")
                font.pixelSize: 12
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            CustomButton {
                id: to2Dbutton
                colorPressed: "#ce4500"
                colorMouseOver: "#b46843"
                colorDefault: "#66707b"
                text: qsTr("To 2D")
                Layout.preferredHeight: 30
                Layout.preferredWidth: 100
                Layout.fillWidth: false
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: fileExport2D.open()
            }

            CustomButton {
                id: to3Dbutton
                colorPressed: "#ce4500"
                colorMouseOver: "#b46843"
                colorDefault: "#66707b"
                text: qsTr("To 3D")
                Layout.preferredHeight: 30
                Layout.preferredWidth: 100
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: fileExport3D.open()
            }

            Text {
                id: text2
                color: "#ffffff"
                text: qsTr("Results export")
                font.pixelSize: 12
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            }

            CustomButton {
                id: resultsButton
                colorPressed: "#ce4500"
                colorMouseOver: "#b46843"
                colorDefault: "#66707b"
                text: qsTr("Results")
                Layout.preferredHeight: 30
                Layout.preferredWidth: 100
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                onClicked: resultsExport.open()
            }
        }
    }
    Connections {
        target: backend
    }

}


/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:5}
}
##^##*/
