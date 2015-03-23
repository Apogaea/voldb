describe("Shift.isClaimable", function() {
  it("should not be claimable if locked", function() {
    var shift = new app.Shift({is_locked: true, has_open_slots: false});
    expect(shift.isClaimable()).toBe(false);
  });

  it("should not be claimable if locked even if has open slots", function() {
    var shift = new app.Shift({is_locked: true, has_open_slots: true});
    expect(shift.isClaimable()).toBe(false);
  });

  it("should not be claimable if no open slots and not locked", function() {
    var shift = new app.Shift({is_locked: false, has_open_slots: false});
    expect(shift.isClaimable()).toBe(false);
  });

  it("should be claimable if unlocked and has open slots", function() {
    var shift = new app.Shift({is_locked: false, has_open_slots: true});
    expect(shift.isClaimable()).toBe(true);
  });
});

