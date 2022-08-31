import QtQuick 2.15
import QtQuick.Controls 2.15
import "../controls"
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.0

Item {
    id: item1
    height: 600

    Rectangle {
        id: rectangle
        color: "#2d3439"
        anchors.fill: parent


        Rectangle {
            id: rectangle2
            color: "#282e32"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.horizontalCenter
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10
            anchors.rightMargin: 10
            Layout.fillWidth: true

            ColumnLayout {
                id: solveLayout
                anchors.fill: parent
                Layout.margins: 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 7


                Text {
                    id: text1
                    color: "#ffffff"
                    text: qsTr("SOLVE")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.topMargin: 10
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                Text {
                    id: text2
                    color: "#ffffff"
                    text: qsTr("Choose analysis type")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                RowLayout {
                    id: rowLayout2
                    width: 250
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Layout.fillWidth: false

                    CustomRadioButton {
                        id: linearStaticBtn
                        setText: "Linear Static"
                    }
                    CustomRadioButton {
                        id: nonlinearStaticBtn
                        checked: false
                        setText: "Nonlinear Static"
                    }
                }

                Text {
                    id: text6
                    color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                    text: qsTr("Control method")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                RowLayout {
                    id: rowLayout3
                    width: 250
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Layout.fillWidth: false

                    CustomRadioButton {
                        id: forceControl
                        checkable: nonlinearStaticBtn.checked ? true : false
                        checked: nonlinearStaticBtn.checked ? true : false
                        setText: "Force Control"
                    }

                    CustomRadioButton {
                        id: disControl
                        checkable: nonlinearStaticBtn.checked ? true : false
                        checked: false
                        setText: "Displacement Control"
                    }
                }

                Text {
                    id: text3
                    color: nonlinearStaticBtn.checked & forceControl.checked ? "#ffffff" : "#808a95"
                    text: qsTr("Force control parameters")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.topMargin: 10
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                RowLayout {
                    id: rowLayout1
                    width: 100
                    height: 80
                    Layout.rightMargin: 10
                    Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                    Text {
                        id: text5
                        color: nonlinearStaticBtn.checked & forceControl.checked ? "#ffffff" : "#808a95"
                        text: "Number of increments"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.topMargin: 10
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    CustomSpinBox {
                        id: incrementsNum
                        height: 20
                        stepSize: 1
                        Layout.preferredHeight: 30
                        enabled: nonlinearStaticBtn.checked & forceControl.checked ? true : false
                        value: 10
                        editable: true
                        to: 100
                        from: 1
                    }
                    Layout.fillWidth: true
                    spacing: 15
                    Layout.bottomMargin: 0
                    Layout.fillHeight: false
                }

                Text {
                    id: text12
                    color: nonlinearStaticBtn.checked & disControl.checked ? "#ffffff" : "#808a95"
                    text: qsTr("Displacement control parameters")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.fillWidth: true
                    Layout.topMargin: 10
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.fillHeight: false
                }

                RowLayout {
                    id: rowLayout7
                    width: 100
                    height: 80
                    Layout.rightMargin: 10
                    Layout.fillWidth: true
                    spacing: 15
                    Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                    Text {
                        id: text13
                        color: nonlinearStaticBtn.checked & disControl.checked ? "#ffffff" : "#808a95"
                        text: qsTr("Displacement increment value [m]")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.topMargin: 10
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.fillHeight: false
                    }

                    CustomTextField {
                        id: incValue
                        text: "1"
                        Layout.fillWidth: true
                        placeholderText: ""
                        colorText: nonlinearStaticBtn.checked & disControl.checked ? "#ffffff" : "#808a95"
                        colorDefault: "#1b1f22"
                        colorOnFocus: nonlinearStaticBtn.checked & disControl.checked ? "#363f44" : "#1b1f22"
                        readOnly: nonlinearStaticBtn.checked & disControl.checked ? false : true
                        colorMouseOver: nonlinearStaticBtn.checked & disControl.checked ? "#202528" : "#1b1f22"
                    }
                    Layout.fillHeight: true
                    Layout.bottomMargin: 0
                }

                RowLayout {
                    id: rowLayout8
                    width: 100
                    height: 80
                    Layout.rightMargin: 10
                    Layout.fillWidth: true
                    spacing: 15
                    Layout.alignment: Qt.AlignLeft | Qt.AlignBottom
                    Text {
                        id: text14
                        color: nonlinearStaticBtn.checked & disControl.checked ? "#ffffff" : "#808a95"
                        text: qsTr("Degree of freedom to control")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillWidth: true
                        Layout.topMargin: 10
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.fillHeight: false
                    }

                    CustomTextField {
                        id: dofControl
                        text: "1"
                        Layout.fillWidth: true
                        placeholderText: ""
                        colorText: nonlinearStaticBtn.checked & disControl.checked ? "#ffffff" : "#808a95"
                        colorDefault: "#1b1f22"
                        colorOnFocus: nonlinearStaticBtn.checked & disControl.checked ? "#363f44" : "#1b1f22"
                        colorMouseOver: nonlinearStaticBtn.checked & disControl.checked ? "#202528" : "#1b1f22"
                        readOnly: nonlinearStaticBtn.checked & disControl.checked ? false : true
                    }
                    Layout.fillHeight: true
                    Layout.bottomMargin: 0
                }

                Text {
                    id: text8
                    color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                    text: qsTr("Convergance criteria")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }


                RowLayout {
                    id: rowLayout
                    width: 100
                    height: 80
                    Layout.rightMargin: 10
                    Layout.bottomMargin: 0
                    spacing: 15
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Layout.fillHeight: false
                    Layout.fillWidth: true

                    Text {
                        id: text4
                        color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        text: qsTr("Maximum iterations")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.leftMargin: -40
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        Layout.topMargin: 10
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    CustomSpinBox {
                        id: maxIter
                        Layout.preferredHeight: 30
                        enabled: nonlinearStaticBtn.checked ? true : false
                        to: 100
                        from: 1
                        value: 40
                        editable: true
                    }


                }


                RowLayout {
                    id: rowLayout4
                    width: 100
                    height: 80
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Layout.fillWidth: true
                    Layout.rightMargin: 10
                    spacing: 15
                    Layout.fillHeight: true
                    Layout.bottomMargin: 0

                    Text {
                        id: text9
                        color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        text: qsTr("Residual force norm")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.topMargin: 10
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    CustomTextField{
                        id: resNorm
                        text: "1e-06"
                        colorText: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        colorOnFocus: nonlinearStaticBtn.checked ? "#363f44" : "#1b1f22"
                        readOnly: nonlinearStaticBtn.checked ? false : true
                        colorMouseOver: nonlinearStaticBtn.checked ? "#202528" : "#1b1f22"
                        colorDefault: "#1b1f22"
                        placeholderText: ""
                        Layout.fillWidth: true
                        Keys.onEnterPressed: {

                        }
                    }

                }

                RowLayout {
                    id: rowLayout5
                    width: 100
                    height: 80
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Text {
                        id: text10
                        color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        text: qsTr("Displacements norm")
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.topMargin: 10
                        Layout.fillWidth: true
                        Layout.fillHeight: false
                    }

                    CustomTextField {
                        id: disNorm
                        text: "1e-06"
                        colorText: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        colorOnFocus: nonlinearStaticBtn.checked ? "#363f44" : "#1b1f22"
                        readOnly: nonlinearStaticBtn.checked ? false : true
                        colorMouseOver: nonlinearStaticBtn.checked ? "#202528" : "#1b1f22"
                        colorDefault: "#1b1f22"
                        Layout.fillWidth: true
                        placeholderText: ""
                    }
                    Layout.fillWidth: true
                    Layout.rightMargin: 10
                    spacing: 15
                    Layout.bottomMargin: 0
                    Layout.fillHeight: true
                }

                RowLayout {
                    id: rowLayout6
                    width: 100
                    height: 80
                    Layout.fillHeight: true
                    spacing: 15
                    Layout.bottomMargin: 0
                    Layout.rightMargin: 10
                    Text {
                        id: text11
                        color: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        text: "Degree of freedom to track"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        Layout.fillHeight: false
                        Layout.topMargin: 10
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                        Layout.fillWidth: true
                    }

                    CustomTextField {
                        id: dofTrack
                        text: "1"
                        colorText: nonlinearStaticBtn.checked ? "#ffffff" : "#808a95"
                        readOnly: nonlinearStaticBtn.checked ? false : true
                        colorMouseOver: nonlinearStaticBtn.checked ? "#202528" : "#1b1f22"
                        colorDefault: "#1b1f22"
                        placeholderText: ""
                        colorOnFocus: nonlinearStaticBtn.checked ? "#363f44" : "#1b1f22"
                        Layout.fillWidth: true
                    }
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    Layout.fillWidth: true
                }

                CustomButton {
                    id: solveBtn
                    text: qsTr("Solve")
                    Layout.preferredHeight: 30
                    colorPressed: "#ce4500"
                    colorMouseOver: "#b46843"
                    colorDefault: "#66707b"
                    Layout.preferredWidth: 100
                    Layout.fillHeight: false
                    Layout.fillWidth: false
                    Layout.bottomMargin: 10
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
                    onClicked: if (nonlinearStaticBtn.checked & forceControl.checked){
                                   backend.solveModelForceNonlinear(incrementsNum.value, maxIter.value, resNorm.text, disNorm.text, dofTrack.text)
                               }else if (nonlinearStaticBtn.checked & disControl.checked){
                                   backend.solveModelDisNonlinear(incValue.text, maxIter.value, resNorm.text, disNorm.text, dofTrack.text,dofControl.text)
                               }else{
                                   backend.solveModelLinear()
                               }
                }





            }
        }

        Rectangle {
            id: rectangle1
            x: 368
            width: 3
            color: "#8599a6"
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            id: rectangle3
            x: 400
            y: 0
            color: "#282e32"
            radius: 10
            anchors.left: parent.horizontalCenter
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 10
            anchors.bottomMargin: 10
            anchors.topMargin: 10
            anchors.leftMargin: 10
            Layout.margins: 10

            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: rightSide
                anchors.fill: parent

                Text {
                    id: text7
                    color: "#ffffff"
                    text: qsTr("RESULTS")
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    Layout.topMargin: 10
                    Layout.fillWidth: true
                    Layout.fillHeight: false
                }

                Flickable {
                    id: flickable
                    width: 300
                    height: 300
                    ScrollBar.vertical: ScrollBar {
                    }
                    TextArea.flickable: TextArea {
                        id: resultsField
                        color: "#ffffff"
                        anchors.fill: parent
                        selectByMouse: true
                        placeholderText: qsTr("")
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        readOnly: true
                        Layout.fillWidth: true
                        font.pointSize: 10
                        Layout.fillHeight: true
                        selectionColor: "#ce6835"
                        anchors.rightMargin: 20
                    }
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                }
            }
        }
    }

    Connections {
        target: backend

        function onReadResults(results){
            resultsField.text = results
        }
    }
}





