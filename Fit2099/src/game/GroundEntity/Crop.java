package game.GroundEntity;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
/**
 * Abstract class representing the BaseClass of Crops. Extends Ground
 * @author Angus Ashby
 */
public abstract class Crop extends Ground {
    public Crop(char displayChar) {
        super(displayChar, "Crop");
    }
    public abstract void blooms(Location location, Actor actor, GameMap map);
    public abstract void tick(Location location);
    public int getStaminaCost(){
        return 0;
    }
}