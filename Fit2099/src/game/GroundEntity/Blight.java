package game.GroundEntity;

import edu.monash.fit2099.engine.positions.Ground;

/**
 * A class representing a blight covering the ground of the valley.
 * @author Adrian Kristanto
 * @Edited by Angus Ashby
 */
public class Blight extends Ground {
    public Blight() {
        super('x', "Blight");
        this.addCapability(EntityType.CURSED);
    }
}
