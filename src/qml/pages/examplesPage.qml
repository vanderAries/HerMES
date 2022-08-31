import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../controls"

Item {

    Rectangle {
        id: rectangle
        color: "#2d3439"
        anchors.fill: parent

        ColumnLayout {
            id: columnLayout
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.verticalCenter
            spacing: 10
            anchors.bottomMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.leftMargin: 0

            Text {
                id: text1
                color: "#ffffff"
                text: qsTr("AVALIABLE EXAMPLES")
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.fillHeight: false
                Layout.topMargin: 30
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                Layout.fillWidth: true
            }

            RowLayout {
                id: rowLayout
                Layout.preferredHeight: 100
                Layout.preferredWidth: 600
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop

                CustomButton {
                    id: vonMisesbutton
                    width: 100
                    height: 30
                    text: qsTr("Von Mises Truss")
                    font.pointSize: 12
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    colorPressed: "#ce4500"
                    colorMouseOver: "#b46843"
                    colorDefault: "#66707b"
                    Layout.fillHeight: false
                    Layout.fillWidth: false
                    Layout.preferredHeight: 50
                    Layout.preferredWidth: 150
                    anchors.leftMargin: 50
                    anchors.topMargin: 50
                    onClicked: {
                        btnModel.isActiveMenu = true
                        btnSolve.isActiveMenu = false
                        btnExamples.isActiveMenu = false
                        btnExport.isActiveMenu = false
                        btnSettings.isActiveMenu = false
                        pageModel.visible = true
                        pageSolve.visible = false
                        pageExamples.visible = false
                        pageExport.visible = false
                        pageSettings.visible = false
                        backend.importVonMises()
                    }

                }

                CustomButton {
                    id: spaceTrussButton
                    width: 100
                    height: 30
                    text: qsTr("Space Truss")
                    font.pointSize: 12
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    anchors.topMargin: 50
                    anchors.leftMargin: 50
                    Layout.fillHeight: false
                    colorMouseOver: "#b46843"
                    colorDefault: "#66707b"
                    Layout.preferredWidth: 150
                    colorPressed: "#ce4500"
                    Layout.preferredHeight: 50
                    Layout.fillWidth: false
                    onClicked: {
                        btnModel.isActiveMenu = true
                        btnSolve.isActiveMenu = false
                        btnExamples.isActiveMenu = false
                        btnExport.isActiveMenu = false
                        btnSettings.isActiveMenu = false
                        pageModel.visible = true
                        pageSolve.visible = false
                        pageExamples.visible = false
                        pageExport.visible = false
                        pageSettings.visible = false
                        backend.importSpaceTruss()
                    }
                }

                CustomButton {
                    id: domeButton
                    width: 100
                    height: 30
                    text: qsTr("Dome")
                    font.pointSize: 12
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.bottomMargin: 0
                    anchors.topMargin: 50
                    anchors.leftMargin: 50
                    Layout.fillHeight: false
                    colorMouseOver: "#b46843"
                    colorDefault: "#66707b"
                    Layout.preferredWidth: 150
                    colorPressed: "#ce4500"
                    Layout.preferredHeight: 50
                    Layout.fillWidth: false
                    onClicked: {
                        btnModel.isActiveMenu = true
                        btnSolve.isActiveMenu = false
                        btnExamples.isActiveMenu = false
                        btnExport.isActiveMenu = false
                        btnSettings.isActiveMenu = false
                        pageModel.visible = true
                        pageSolve.visible = false
                        pageExamples.visible = false
                        pageExport.visible = false
                        pageSettings.visible = false
                        backend.importDome()
                    }
                }
            }


        }
    }
    Connections {
        target: backend
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:1.1;height:480;width:640}
}
##^##*/
