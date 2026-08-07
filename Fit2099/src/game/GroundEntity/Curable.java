package game.GroundEntity;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
/**
 * Interface to represent Curable Objects
 * @author Angus Ashby
 */
public interface Curable {
    void cure(Actor user, GameMap map);
}
