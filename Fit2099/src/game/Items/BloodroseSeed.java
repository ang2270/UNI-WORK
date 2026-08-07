package game.Items;

import game.GroundEntity.Bloodrose;
import game.GroundEntity.Crop;
/**
 * Subclass of SeedItem this represents a BloodRoseSeed item
 * @author Angus Ashby
 */
public class BloodroseSeed extends SeedItem {
    public BloodroseSeed() {
        super("Bloodrose Seed", '*', true, new Bloodrose(), "Bloodrose");
    }
    /**
     * Returns a new instance of the Plant this Seed Grows into when planted
     */
    @Override
    protected Crop newInstanceOfCrop() {
        return new Bloodrose();
    }

}