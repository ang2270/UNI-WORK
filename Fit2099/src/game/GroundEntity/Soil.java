package game.GroundEntity;

import edu.monash.fit2099.engine.positions.Ground;

/**
 * A class representing the soil in the valley
 * @author Adrian Kristanto
 */
public class Soil extends Ground {
    public Soil() {
        super('.', "Soil");
        this.addCapability(EntityType.SOIL);
    }
}
