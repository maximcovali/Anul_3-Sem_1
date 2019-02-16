package ro.ase.acs.coolweatherid;

import java.io.Serializable;

public class Location implements Serializable {
    public String city;
    public String country;

    @Override
    public String toString() {
        return city + ", " + country;
    }
}
