package com.example.demo;

import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import java.io.FileInputStream;
import java.util.concurrent.atomic.AtomicInteger;

public class Nõudepesumasin extends Application {

    private ImageView taustapilt;

    @Override
    public void start(Stage stage) throws Exception {
        //PÕHIPAAN JA SÄTTED
        StackPane juurikas = new StackPane();
        HBox nupuJuur = new HBox();
        HBox käivitusJuur = new HBox();
        VBox taustapiltJuur = new VBox();
        HBox tekstiJuur = new HBox();

        nupuJuur.setMaxSize(Region.USE_PREF_SIZE, Region.USE_PREF_SIZE);
        käivitusJuur.setMaxSize(Region.USE_PREF_SIZE, Region.USE_PREF_SIZE);
        tekstiJuur.setMaxSize(Region.USE_PREF_SIZE, Region.USE_PREF_SIZE);

        StackPane.setAlignment(nupuJuur, Pos.CENTER);
        StackPane.setAlignment(tekstiJuur, Pos.TOP_CENTER);
        StackPane.setAlignment(käivitusJuur, Pos.BOTTOM_CENTER);
        juurikas.getChildren().addAll(taustapiltJuur, tekstiJuur, nupuJuur, käivitusJuur);

        Scene stseen = new Scene(juurikas,400, 400);
        stage.setMinHeight(300);
        stage.setMinWidth(300);

        //TAUSTAPILT
        Image mainTaustapilt = null;
        mainTaustapilt = new Image(new FileInputStream("mainTaustapilt.png"));
        this.taustapilt = new ImageView(mainTaustapilt);
        taustapilt.setFitWidth(400);
        taustapilt.setFitHeight(400);
        taustapilt.setPreserveRatio(false);

        stseen.widthProperty().addListener(new ChangeListener<Number>() {
            @Override
            public void changed(ObservableValue<? extends Number> observableValue, Number number, Number t1) {
                taustapilt.setFitWidth(stseen.getWidth());
            }
        });
        stseen.heightProperty().addListener(new ChangeListener<Number>() {
            @Override
            public void changed(ObservableValue<? extends Number> observableValue, Number number, Number t1) {
                taustapilt.setFitHeight(stseen.getHeight());
            }
        });

        //NUPUD JA TEKSTIAVAD
        Button ecopesuNupp = new Button("ECOpesu");
        Button tavapesuNupp = new Button("Tavapesu");
        Button süvapesuNupp = new Button("Süvapesu");
        Button käivitusNupp = new Button("Käivita nõudepesumasin");

        TextField nõudehulk = new TextField();
        nõudehulk.setPrefColumnCount(2);
        TextField tablett = new TextField();
        tablett.setPrefColumnCount(2);

        AtomicInteger pesurežiim = new AtomicInteger();
        ecopesuNupp.setOnAction(actionEvent -> {
            ecopesuNupp();
            pesurežiim.set(1);
        });

        tavapesuNupp.setOnAction(actionEvent -> {
            tavapesuNupp();
            pesurežiim.set(2);
        });
        süvapesuNupp.setOnAction(actionEvent -> {
            süvapesuNupp();
            pesurežiim.set(3);
        });
        käivitusNupp.setOnAction(e -> {
            int nõudeArv = Integer.parseInt(nõudehulk.getText());
            int tabletiKasutus = Integer.parseInt(tablett.getText());
            int pesureziim = pesurežiim.intValue();
            if (pesureziim == 1) { // ECOpesu.
                if (nõudeArv > 0) {
                    System.out.println("Pesumasin töötab 60 minutit.");
                    int võimalus = (int) ((Math.random() * (100.0) + 1.0)); // Väljastab suvalise arvu 1-100ni.
                    if (võimalus > 50) { // ECOpesu korral 50% juhtudest ei saa kõik nõud puhtaks.
                        System.out.println("ECOrežiim ei suutnud nõusid täiesti puhtaks teha!");
                    } else if (tabletiKasutus == 0) {
                        System.out.println("Nõud ei saanud täiesti puhtaks, kuna Te ei lisanud tabletti!");
                    } else if (nõudeArv > 15) {
                        System.out.println("Nõusid oli liiga palju! Nõud ei saanud täielikult puhtaks!");
                    } else {
                        System.out.println("Nõud said pestud!");
                    }
                } else {
                    System.out.println("Nõudepesumasin on tühi. Palun lisage nõusid enne käivitamist.");
                }
            }
            if (pesureziim == 2) { // Tavapesu.
                if (nõudeArv > 0) {
                    System.out.println("Pesumasin töötab 90 minutit.");
                    int võimalus = (int) ((Math.random() * (100.0) + 1.0)); // Väljastab suvalise arvu 1-100ni.
                    if (võimalus > 75) { // Tavapesu korral 25% juhtudest ei saa kõik nõud puhtaks.
                        System.out.println("Tavapesu režiim ei suutnud nõusid täiesti puhtaks teha!");
                    } else if (tabletiKasutus == 0) {
                        System.out.println("Nõud ei saanud täiesti puhtaks, kuna Te ei lisanud tabletti!");
                    } else if (nõudeArv > 25) {
                        System.out.println("Nõusid oli liiga palju! Nõud ei saanud täielikult puhtaks!");
                    } else {
                        System.out.println("Nõud said pestud!");
                    }
                } else {
                    System.out.println("Nõudepesumasin on tühi. Palun lisage nõusid enne käivitamist.");
                }
            }
            if (pesureziim == 3) { // Süvapesu.
                if (nõudeArv > 0) {
                    System.out.println("Nõudepesumasin töötab 120 minutit.");
                    int võimalus = (int) ((Math.random() * (100.0) + 1.0)); // Väljastab suvalise arvu 1-100ni.
                    if (võimalus > 95) { // Süvapesu korral 5% juhtudest ei saa kõik nõud puhtaks.
                        System.out.println("Süvapesu režiim ei suutnud nõusid täiesti puhtaks teha!");
                    } else if (tabletiKasutus == 0) {
                        System.out.println("Nõud ei saanud täiesti puhtaks, kuna Te ei lisanud tabletti!");
                    } else {
                        System.out.println("Nõud said pestud!");
                    }
                } else {
                    System.out.println("Nõudepesumasin on tühi. Palun lisage nõusid enne käivitamist.");
                }
            }

        });

        //LISAB TAUSTAPILDI
        taustapiltJuur.getChildren().addAll(taustapilt);

        //LISAB NUPUD
        nupuJuur.getChildren().addAll(ecopesuNupp,tavapesuNupp,süvapesuNupp);
        nupuJuur.setSpacing(10);
        käivitusJuur.getChildren().addAll(käivitusNupp);

        //LISAB TEKSIAVAD
        Label nõudehulkKiri = new Label("Nõudehulk:");
        Label tablettKiri = new Label("Tabletid:");
        tekstiJuur.getChildren().addAll(nõudehulkKiri, nõudehulk, tablettKiri, tablett);
        tekstiJuur.setSpacing(10);


        //NÄITAB TULEMUST
        stage.setScene(stseen);
        stage.setTitle("Nõudepesumasin");
        stage.show();
    }


    private void ecopesuNupp() {
        System.out.println("Valisite ECOpesu");
    }
    private void tavapesuNupp() {
        System.out.println("Valisite tavapesu");
    }
    private void süvapesuNupp() {
        System.out.println("Valisite süvapesu");
    }
    public static void main(String[] args) {
        launch(args);
    }
}
