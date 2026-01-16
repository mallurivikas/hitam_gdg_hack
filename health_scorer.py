"""
Health Scorer - Combines individual health risk scores into overall health assessment
"""


class HealthScorer:
    def __init__(self):
        # Weights for each health condition (must sum to 1.0)
        # These reflect medical severity/importance
        self.weights = {
            'heart': 0.25,        # Cardiovascular disease - most critical
            'diabetes': 0.25,     # Diabetes - high impact on overall health
            'hypertension': 0.25, # High blood pressure - significant health risk
            'obesity': 0.25       # Obesity - important but often manageable
        }
        
        # Risk level thresholds
        self.risk_thresholds = {
            'low': 30,
            'moderate': 50,
            'high': 70,
            'critical': 85
        }
    
    def calculate_composite_risk(self, risk_scores):
        """
        Calculate weighted composite risk score
        
        Args:
            risk_scores (dict): Dictionary with keys: heart, diabetes, hypertension, obesity
                               Values should be risk percentages (0-100)
        
        Returns:
            float: Composite risk score (0-100)
        """
        composite_risk = (
            risk_scores['heart'] * self.weights['heart'] +
            risk_scores['diabetes'] * self.weights['diabetes'] +
            risk_scores['hypertension'] * self.weights['hypertension'] +
            risk_scores['obesity'] * self.weights['obesity']
        )
        
        return round(composite_risk, 2)
    
    def calculate_health_score(self, risk_scores):
        """
        Calculate overall health score (inverse of composite risk)
        
        Args:
            risk_scores (dict): Dictionary with risk percentages
        
        Returns:
            float: Health score (0-100, where 100 is perfect health)
        """
        composite_risk = self.calculate_composite_risk(risk_scores)
        health_score = 100 - composite_risk
        
        return round(health_score, 2)
    
    def get_risk_level(self, risk_score):
        """
        Determine risk level category
        
        Args:
            risk_score (float): Risk percentage (0-100)
        
        Returns:
            str: Risk level (low, moderate, high, critical)
        """
        if risk_score < self.risk_thresholds['low']:
            return 'low'
        elif risk_score < self.risk_thresholds['moderate']:
            return 'moderate'
        elif risk_score < self.risk_thresholds['high']:
            return 'high'
        elif risk_score < self.risk_thresholds['critical']:
            return 'very high'
        else:
            return 'critical'
    
    def get_health_grade(self, health_score):
        """
        Convert health score to letter grade
        
        Args:
            health_score (float): Health score (0-100)
        
        Returns:
            str: Letter grade (A+ to F)
        """
        if health_score >= 90:
            return 'A+'
        elif health_score >= 80:
            return 'A'
        elif health_score >= 70:
            return 'B'
        elif health_score >= 60:
            return 'C'
        elif health_score >= 50:
            return 'D'
        else:
            return 'F'
    
    def generate_recommendations(self, risk_scores):
        """
        Generate personalized health recommendations based on risk scores
        Uses actual risk thresholds defined in the class, not hardcoded values
        
        Args:
            risk_scores (dict): Individual risk scores
        
        Returns:
            list: List of recommendation strings
        """
        recommendations = []
        
        # Get risk levels for each condition
        heart_level = self.get_risk_level(risk_scores['heart'])
        diabetes_level = self.get_risk_level(risk_scores['diabetes'])
        hypertension_level = self.get_risk_level(risk_scores['hypertension'])
        obesity_level = self.get_risk_level(risk_scores['obesity'])
        
        # Heart disease recommendations - based on actual risk level
        if heart_level in ['critical', 'very high']:
            recommendations.append(f"🫀 HEART HEALTH: {risk_scores['heart']:.1f}% risk - CRITICAL. Seek immediate medical attention.")
            recommendations.append("   - Schedule urgent cardiology appointment")
            recommendations.append("   - Monitor blood pressure and cholesterol daily")
            recommendations.append("   - Avoid strenuous activities until cleared by doctor")
        elif heart_level == 'high':
            recommendations.append(f"🫀 HEART HEALTH: {risk_scores['heart']:.1f}% risk - High. Consult a cardiologist soon.")
            recommendations.append("   - Monitor blood pressure and cholesterol regularly")
            recommendations.append("   - Engage in 30+ minutes of cardio exercise daily")
            recommendations.append("   - Reduce saturated fat and sodium intake")
        elif heart_level == 'moderate':
            recommendations.append(f"🫀 HEART HEALTH: {risk_scores['heart']:.1f}% risk - Moderate. Take preventive measures.")
            recommendations.append("   - Regular cardiovascular exercise (walking, cycling)")
            recommendations.append("   - Maintain healthy weight and cholesterol levels")
        elif heart_level == 'low':
            recommendations.append(f"🫀 HEART HEALTH: {risk_scores['heart']:.1f}% risk - Low. Keep up the good work!")
            recommendations.append("   - Continue healthy lifestyle habits")
        
        # Diabetes recommendations - based on actual risk level
        if diabetes_level in ['critical', 'very high']:
            recommendations.append(f"🩸 DIABETES: {risk_scores['diabetes']:.1f}% risk - CRITICAL. Get tested immediately.")
            recommendations.append("   - Schedule urgent blood glucose test (HbA1c)")
            recommendations.append("   - Strictly limit sugar and refined carbs")
            recommendations.append("   - Consider consulting an endocrinologist")
        elif diabetes_level == 'high':
            recommendations.append(f"🩸 DIABETES: {risk_scores['diabetes']:.1f}% risk - High. Get blood sugar tested.")
            recommendations.append("   - Monitor glucose levels regularly")
            recommendations.append("   - Reduce sugar and refined carbohydrate intake")
            recommendations.append("   - Increase fiber-rich foods and whole grains")
        elif diabetes_level == 'moderate':
            recommendations.append(f"🩸 DIABETES: {risk_scores['diabetes']:.1f}% risk - Moderate. Focus on prevention.")
            recommendations.append("   - Maintain healthy weight through diet and exercise")
            recommendations.append("   - Limit sugary beverages and processed foods")
        elif diabetes_level == 'low':
            recommendations.append(f"🩸 DIABETES: {risk_scores['diabetes']:.1f}% risk - Low. Excellent!")
            recommendations.append("   - Maintain balanced diet with controlled portions")
        
        # Hypertension recommendations - based on actual risk level
        if hypertension_level in ['critical', 'very high']:
            recommendations.append(f"💊 BLOOD PRESSURE: {risk_scores['hypertension']:.1f}% risk - CRITICAL. Check BP now!")
            recommendations.append("   - Measure blood pressure immediately")
            recommendations.append("   - Strictly limit sodium (<1500mg/day)")
            recommendations.append("   - Avoid stress and seek medical help")
        elif hypertension_level == 'high':
            recommendations.append(f"💊 BLOOD PRESSURE: {risk_scores['hypertension']:.1f}% risk - High. Monitor BP regularly.")
            recommendations.append("   - Reduce sodium intake (< 2000mg/day)")
            recommendations.append("   - Practice stress management techniques")
            recommendations.append("   - Avoid excessive alcohol and caffeine")
        elif hypertension_level == 'moderate':
            recommendations.append(f"💊 BLOOD PRESSURE: {risk_scores['hypertension']:.1f}% risk - Moderate. Take preventive steps.")
            recommendations.append("   - Maintain regular sleep schedule (7-8 hours)")
            recommendations.append("   - Engage in regular physical activity")
        elif hypertension_level == 'low':
            recommendations.append(f"💊 BLOOD PRESSURE: {risk_scores['hypertension']:.1f}% risk - Low. Great!")
            recommendations.append("   - Continue healthy habits and regular exercise")
        
        # Obesity recommendations - based on actual risk level
        if obesity_level in ['critical', 'very high']:
            recommendations.append(f"⚖️ WEIGHT MANAGEMENT: {risk_scores['obesity']:.1f}% risk - CRITICAL. Urgent action needed.")
            recommendations.append("   - Consult healthcare provider for weight management plan")
            recommendations.append("   - Consider supervised weight loss program")
            recommendations.append("   - Address underlying health conditions")
        elif obesity_level == 'high':
            recommendations.append(f"⚖️ WEIGHT MANAGEMENT: {risk_scores['obesity']:.1f}% risk - High. Action needed.")
            recommendations.append("   - Consult a nutritionist for personalized diet plan")
            recommendations.append("   - Aim for gradual weight loss (1-2 lbs/week)")
            recommendations.append("   - Combine cardio and strength training exercises")
        elif obesity_level == 'moderate':
            recommendations.append(f"⚖️ WEIGHT MANAGEMENT: {risk_scores['obesity']:.1f}% risk - Moderate. Room for improvement.")
            recommendations.append("   - Maintain calorie balance and portion control")
            recommendations.append("   - Increase daily physical activity")
        elif obesity_level == 'low':
            recommendations.append(f"⚖️ WEIGHT MANAGEMENT: {risk_scores['obesity']:.1f}% risk - Low. Healthy weight!")
            recommendations.append("   - Maintain current healthy eating patterns")
        
        # General recommendations only if ALL risks are low
        if all(level == 'low' for level in [heart_level, diabetes_level, hypertension_level, obesity_level]):
            recommendations.append("✅ EXCELLENT OVERALL HEALTH STATUS!")
            recommendations.append("   - Continue maintaining healthy lifestyle habits")
            recommendations.append("   - Regular health checkups for prevention")
        
        return recommendations
    
    def generate_health_report(self, risk_scores):
        """
        Generate comprehensive health assessment report
        
        Args:
            risk_scores (dict): Individual risk scores
        
        Returns:
            dict: Complete health report with scores, grades, and recommendations
        """
        composite_risk = self.calculate_composite_risk(risk_scores)
        health_score = self.calculate_health_score(risk_scores)
        risk_level = self.get_risk_level(composite_risk)
        health_grade = self.get_health_grade(health_score)
        recommendations = self.generate_recommendations(risk_scores)
        
        report = {
            'individual_risks': {
                'heart_disease': {
                    'score': round(risk_scores['heart'], 2),
                    'level': self.get_risk_level(risk_scores['heart'])
                },
                'diabetes': {
                    'score': round(risk_scores['diabetes'], 2),
                    'level': self.get_risk_level(risk_scores['diabetes'])
                },
                'hypertension': {
                    'score': round(risk_scores['hypertension'], 2),
                    'level': self.get_risk_level(risk_scores['hypertension'])
                },
                'obesity': {
                    'score': round(risk_scores['obesity'], 2),
                    'level': self.get_risk_level(risk_scores['obesity'])
                }
            },
            'composite_risk': composite_risk,
            'health_score': health_score,
            'risk_level': risk_level,
            'health_grade': health_grade,
            'recommendations': recommendations,
            'weights_used': self.weights
        }
        
        return report
    
    def print_health_report(self, report):
        """
        Print formatted health report to console
        
        Args:
            report (dict): Health report from generate_health_report()
        """
        print("\n" + "="*80)
        print("                    🏥 COMPREHENSIVE HEALTH ASSESSMENT REPORT 🏥")
        print("="*80)
        
        # Overall scores
        print(f"\n📊 OVERALL HEALTH SCORE: {report['health_score']:.1f}/100 (Grade: {report['health_grade']})")
        print(f"⚠️  COMPOSITE RISK LEVEL: {report['composite_risk']:.1f}% ({report['risk_level'].upper()})")
        
        # Individual risk scores
        print("\n" + "-"*80)
        print("📋 INDIVIDUAL HEALTH RISK BREAKDOWN:")
        print("-"*80)
        
        risks = report['individual_risks']
        print(f"  🫀 Heart Disease Risk:    {risks['heart_disease']['score']:>6.1f}%  [{risks['heart_disease']['level'].upper()}]")
        print(f"  🩸 Diabetes Risk:         {risks['diabetes']['score']:>6.1f}%  [{risks['diabetes']['level'].upper()}]")
        print(f"  💊 Hypertension Risk:     {risks['hypertension']['score']:>6.1f}%  [{risks['hypertension']['level'].upper()}]")
        print(f"  ⚖️  Obesity Risk:          {risks['obesity']['score']:>6.1f}%  [{risks['obesity']['level'].upper()}]")
        
        # Weights
        print("\n" + "-"*80)
        print("⚖️  RISK WEIGHTING FACTORS:")
        print("-"*80)
        weights = report['weights_used']
        print(f"  Heart Disease:  {weights['heart']*100:.0f}%")
        print(f"  Diabetes:       {weights['diabetes']*100:.0f}%")
        print(f"  Hypertension:   {weights['hypertension']*100:.0f}%")
        print(f"  Obesity:        {weights['obesity']*100:.0f}%")
        
        # Recommendations
        print("\n" + "-"*80)
        print("💡 PERSONALIZED HEALTH RECOMMENDATIONS:")
        print("-"*80)
        for rec in report['recommendations']:
            print(f"  {rec}")
        
        print("\n" + "="*80)
        print("⚕️  DISCLAIMER: This is an AI-based assessment. Please consult healthcare")
        print("   professionals for medical advice and diagnosis.")
        print("="*80 + "\n")


if __name__ == "__main__":
    # Test the health scorer
    scorer = HealthScorer()
    
    # Example risk scores
    test_scores = {
        'heart': 65.5,
        'diabetes': 42.0,
        'hypertension': 58.3,
        'obesity': 35.0
    }
    
    report = scorer.generate_health_report(test_scores)
    scorer.print_health_report(report)
