package com.example.cristinarichter.cursa;

import java.util.Arrays;
import java.util.Calendar;

public class Cursa {
    private String destinatie;
    private Calendar data;
    private String[] tipTaxi = {"normal", "premium"};
    private float cost;

    // constr default
    public Cursa() {
    }

    // constr param
    public Cursa(String destinatie, Calendar data, String[] tipTaxi, float cost) {
        this.destinatie = destinatie;
        this.data = data;
        this.tipTaxi = tipTaxi;
        this.cost = cost;
    }

    // getters & setters
    public String getDestinatie() {
        return destinatie;
    }

    public void setDestinatie(String destinatie) {
        this.destinatie = destinatie;
    }

    public Calendar getData() {
        return data;
    }

    public void setData(Calendar data) {
        this.data = data;
    }

    public String[] getTipTaxi() {
        return tipTaxi;
    }

    public void setTipTaxi(String[] tipTaxi) {
        this.tipTaxi = tipTaxi;
    }

    public float getCost() {
        return cost;
    }

    public void setCost(float cost) {
        this.cost = cost;
    }

    // toString


    @Override
    public String toString() {
        return "Cursa{" +
                "destinatie='" + destinatie + '\'' +
                ", data=" + data +
                ", tipTaxi=" + Arrays.toString(tipTaxi) +
                ", cost=" + cost +
                '}';
    }
}
